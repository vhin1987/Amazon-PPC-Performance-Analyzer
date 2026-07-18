import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import numpy as np
import threading
import os

class PPCAnalyzerCombined:

    def __init__(self, root):
        self.root = root
        self.root.title("Amazon PPC ACoS Analyzer")
        self.root.geometry("1200x780")
        
        # Configure overall style
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        # Customize Treeview styling for professional tabular layout
        self.style.configure(
            "Treeview", 
            rowheight=26, 
            font=("Arial", 10),
            background="#ffffff",
            fieldbackground="#ffffff"
        )
        self.style.configure(
            "Treeview.Heading", 
            font=("Arial", 10, "bold"), 
            background="#f0f0f0"
        )
        self.style.map("Treeview", background=[("selected", "#0078d7")])

        # State variables
        self.df_raw = None
        self.df_clean_keywords = None
        self.df_asin_placements = None
        self.df_neg = None
        self.raw_file_name = ""

        # ================= TITLE =================
        title = tk.Label(
            root,
            text="Amazon PPC ACoS Analyzer",
            font=("Arial", 22, "bold")
        )
        title.pack(pady=10)

        # ================= FILE ACTIONS PANEL =================
        action_frame = tk.LabelFrame(
            root, 
            text="File Actions Panel", 
            font=("Arial", 10, "bold"), 
            fg="#333333"
        )
        action_frame.pack(fill="x", padx=15, pady=5)

        self.file_path = tk.StringVar()

        # Upload Button
        self.upload_btn = tk.Button(
            action_frame,
            text="📁 Upload Raw Data",
            bg="#0078d7",
            fg="white",
            activebackground="#005a9e",
            activeforeground="white",
            command=self.browse_file,
            font=("Arial", 10, "bold"),
            padx=15,
            pady=3
        )
        self.upload_btn.pack(side="left", padx=10, pady=10)

        # File Path Entry
        self.path_entry = tk.Entry(
            action_frame,
            textvariable=self.file_path,
            width=50,
            font=("Arial", 11),
            state="readonly"
        )
        self.path_entry.pack(side="left", padx=5, ipady=4, pady=10)

        # Process / Run Button
        self.run_btn = tk.Button(
            action_frame,
            text="🚀 Run Analysis",
            bg="#2ba151",
            fg="white",
            activebackground="#1f7a3c",
            activeforeground="white",
            command=self.start_analysis,
            font=("Arial", 10, "bold"),
            padx=15,
            pady=3,
            state="disabled"
        )
        self.run_btn.pack(side="left", padx=10, pady=10)

        # Download Processed Button
        self.download_btn = tk.Button(
            action_frame,
            text="💾 Download Cleaned Data",
            bg="#f2a900",
            fg="black",
            activebackground="#d19200",
            activeforeground="black",
            command=self.download_processed_file,
            font=("Arial", 10, "bold"),
            padx=15,
            pady=3,
            state="disabled"
        )
        self.download_btn.pack(side="right", padx=10, pady=10)

        # ================= PROGRESS =================
        self.progress = ttk.Progressbar(
            root,
            mode="indeterminate"
        )
        self.progress.pack(fill="x", padx=15, pady=5)

        # ================= KPI CARDS =================
        card_frame = tk.Frame(root)
        card_frame.pack(fill="x", padx=5, pady=5)

        self.spend_var = tk.StringVar(value="$0")
        self.sales_var = tk.StringVar(value="$0")
        self.acos_var = tk.StringVar(value="0%")
        self.roas_var = tk.StringVar(value="0")

        cards = [
            ("Total Spend", self.spend_var),
            ("Total Sales", self.sales_var),
            ("ACoS", self.acos_var),
            ("ROAS", self.roas_var)
        ]

        for text, var in cards:
            frame = tk.LabelFrame(
                card_frame, 
                text=text, 
                font=("Arial", 10, "bold"),
                fg="#333333"
            )
            frame.pack(side="left", padx=10, fill="both", expand=True)

            tk.Label(
                frame,
                textvariable=var,
                font=("Arial", 18, "bold"),
                fg="#0078d7" if "Sales" in text or "ROAS" in text else "#d83b01" if "Spend" in text else "#333333"
            ).pack(pady=15)

        # ================= TABS =================
        self.tabs = ttk.Notebook(root)
        self.tabs.pack(fill="both", expand=True, padx=15, pady=5)

        self.top_tab = tk.Frame(self.tabs)
        self.neg_tab = tk.Frame(self.tabs)

        self.tabs.add(self.top_tab, text="Cleaned Keywords Preview")
        self.tabs.add(self.neg_tab, text="Negative Targets Preview")

        # TABLES WITH SCROLLBARS
        self.top_tree = self.create_scrollable_treeview(self.top_tab)
        self.neg_tree = self.create_scrollable_treeview(self.neg_tab)

        # LOG CONSOLE
        log_frame = tk.LabelFrame(root, text="System Log", font=("Arial", 9, "bold"))
        log_frame.pack(fill="x", padx=15, pady=10)
        
        self.log = tk.Text(
            log_frame, 
            height=5, 
            bg="#1e1e1e", 
            fg="#d4d4d4", 
            insertbackground="white", 
            font=("Consolas", 10)
        )
        self.log.pack(fill="both", expand=True)

    def create_scrollable_treeview(self, parent):
        container = tk.Frame(parent)
        container.pack(fill="both", expand=True)

        tree = ttk.Treeview(container)
        
        vsb = ttk.Scrollbar(container, orient="vertical", command=tree.yview)
        hsb = ttk.Scrollbar(container, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        tree.configure(show="headings")
        return tree

    def write_log(self, msg):
        self.log.insert(tk.END, f"[*] {msg}\n")
        self.log.see(tk.END)

    def browse_file(self):
        file = filedialog.askopenfilename(
            filetypes=[("Excel Files", "*.xlsx *.xls")]
        )
        if file:
            self.file_path.set(file)
            self.raw_file_name = os.path.basename(file)
            self.write_log(f"Uploaded Raw Data File: {self.raw_file_name}")
            self.run_btn.configure(state="normal")
            self.download_btn.configure(state="disabled")

    def start_analysis(self):
        path = self.file_path.get()
        if not path:
            messagebox.showwarning("Warning", "Please upload a raw Excel file first.")
            return
        
        self.progress.start(10)
        self.write_log("Starting background analysis thread...")
        threading.Thread(target=self.run_analysis, args=(path,), daemon=True).start()

    def run_analysis(self, path):
        try:
            # 1. Store completely unedited Raw Data copy
            df_raw = pd.read_excel(path)
            self.df_raw = df_raw.copy()

            # 2. To avoid case & formatting mismatches, find matching columns dynamically
            df = df_raw.copy()
            raw_columns = [str(c).strip() for c in df.columns]

            def find_matching_column(candidates, fallback_name):
                for candidate in candidates:
                    for col in raw_columns:
                        if candidate.lower() in col.lower():
                            return col
                return fallback_name

            # Dynamic column search rules
            portfolio_col_raw = find_matching_column(["portfolio name", "portfolio"], "Portfolio Name")
            campaign_col_raw = find_matching_column(["campaign name", "campaign"], "Campaign Name")
            search_col_raw = find_matching_column(["customer search term", "search term"], "Customer Search Term")
            impressions_col_raw = find_matching_column(["impressions"], "Impressions")
            clicks_col_raw = find_matching_column(["clicks"], "Clicks")
            spend_col_raw = find_matching_column(["spend"], "Spend")
            orders_col_raw = find_matching_column(["orders", "conversions", "purchases"], "7-Day Total Orders (#)")
            sales_col_raw = find_matching_column(["sales", "revenue"], "7-Day Total Sales ($)")

            # Map dynamically discovered column headers to standardized short names
            column_rename_map = {
                portfolio_col_raw: "Portfolio_Name",
                campaign_col_raw: "Campaign_Name",
                search_col_raw: "Search_Term",
                impressions_col_raw: "Impressions",
                clicks_col_raw: "Clicks",
                spend_col_raw: "Spend",
                orders_col_raw: "Orders",
                sales_col_raw: "Sales"
            }

            # Log mappings
            self.write_log(f"Mapping 'Portfolio' to: {portfolio_col_raw}")
            self.write_log(f"Mapping 'Campaign' to: {campaign_col_raw}")
            self.write_log(f"Mapping 'Search Term' to: {search_col_raw}")
            self.write_log(f"Mapping 'Orders' to: {orders_col_raw}")
            self.write_log(f"Mapping 'Sales' to: {sales_col_raw}")

            # Rename columns
            df = df.rename(columns=column_rename_map)

            # Ensure all mapped columns exist in dataset, filling missing ones with default values
            essential_cols = ["Portfolio_Name", "Campaign_Name", "Search_Term", "Impressions", "Clicks", "Spend", "Orders", "Sales"]
            for col in essential_cols:
                if col not in df.columns:
                    if col in ["Portfolio_Name", "Campaign_Name"]:
                        df[col] = "Not Specified"
                    else:
                        df[col] = 0.0

            # Filter down to essential columns
            df = df[essential_cols]

            # Drop empty search rows & clean string values
            df = df.dropna(subset=["Search_Term"])
            df["Search_Term"] = df["Search_Term"].astype(str).str.strip()
            df["Portfolio_Name"] = df["Portfolio_Name"].fillna("Not Specified").astype(str).str.strip()
            df["Campaign_Name"] = df["Campaign_Name"].fillna("Not Specified").astype(str).str.strip()

            # Cast math columns to numerical representations safely
            for num_col in ["Impressions", "Clicks", "Spend", "Orders", "Sales"]:
                df[num_col] = pd.to_numeric(df[num_col], errors='coerce').fillna(0)

            # 3. Aggregate duplicate search terms across matching Portfolio & Campaign dimensions
            df_grouped = df.groupby(["Portfolio_Name", "Campaign_Name", "Search_Term"], as_index=False).agg({
                "Impressions": "sum",
                "Clicks": "sum",
                "Spend": "sum",
                "Orders": "sum",
                "Sales": "sum"
            })

            # 4. Separate competitor ASIN placements from actual text search terms
            is_asin = df_grouped["Search_Term"].str.startswith(("b0", "B0"))
            df_asin_placements = df_grouped[is_asin].copy()
            df_clean_keywords = df_grouped[~is_asin].copy()

            # 5. Calculate clean math metrics on the aggregated data and add targeting recommendations
            for dataset in [df_clean_keywords, df_asin_placements]:
                dataset["CTR"] = (dataset["Clicks"] / dataset["Impressions"]).fillna(0)
                dataset["CPC"] = (dataset["Spend"] / dataset["Clicks"]).fillna(0)
                dataset["CVR"] = (dataset["Orders"] / dataset["Clicks"]).fillna(0)
                dataset["ACoS"] = (dataset["Spend"] / dataset["Sales"]).fillna(0)
                dataset["RoAS"] = (dataset["Sales"] / dataset["Spend"]).fillna(0)
                
                # Apply business logic targeting recommendations
                conditions = [
                    (dataset["Sales"] == 0) & (dataset["Spend"] > 10.0),                     # Negative Targeting
                    (dataset["Sales"] > 0) & (dataset["ACoS"] < 0.30),                       # Keyword Harvesting (profitable keyword under 30% acos)
                    (dataset["Sales"] > 0) & (dataset["ACoS"] >= 0.30),                      # Optimize Keyword (active, but acos is equal or over 30%)
                ]
                choices = ["Negative targeting", "Keyword Harvesting", "Optimize keyword"]
                dataset["Recommendation"] = np.select(conditions, choices, default="Under Threshold")

                # Round clean decimals
                dataset[["CTR", "CVR", "ACoS"]] = dataset[["CTR", "CVR", "ACoS"]].round(4)
                dataset[["Spend", "Sales", "CPC", "RoAS"]] = dataset[["Spend", "Sales", "CPC", "RoAS"]].round(2)

            # 6. Sort both datasets by Spend descending
            df_clean_keywords = df_clean_keywords.sort_values(by="Spend", ascending=False)
            df_asin_placements = df_asin_placements.sort_values(by="Spend", ascending=False)

            # 7. Extract Negative Targets (Waste keywords: Spend > $10 and 0 Sales)
            df_neg = df_clean_keywords[df_clean_keywords["Recommendation"] == "Negative targeting"].copy()

            # Save state variables
            self.df_clean_keywords = df_clean_keywords
            self.df_asin_placements = df_asin_placements
            self.df_neg = df_neg

            # Aggregations for UI display
            total_spend = df_clean_keywords["Spend"].sum() + df_asin_placements["Spend"].sum()
            total_sales = df_clean_keywords["Sales"].sum() + df_asin_placements["Sales"].sum()
            overall_acos = (total_spend / total_sales * 100) if total_sales > 0 else 0
            overall_roas = (total_sales / total_spend) if total_spend > 0 else 0

            results = {
                "spend": f"${total_spend:,.2f}",
                "sales": f"${total_sales:,.2f}",
                "acos": f"{overall_acos:.2f}%",
                "roas": f"{overall_roas:.2f}",
                "clean_kws": df_clean_keywords.head(25),  # Preview top 25
                "neg_kws": df_neg
            }

            self.root.after(0, self.update_ui_on_success, results)

        except PermissionError:
            error_msg = "Permission Denied: Please close any open instances of your processed Excel sheets and try again!"
            self.root.after(0, self.update_ui_on_failure, error_msg)
        except Exception as e:
            self.root.after(0, self.update_ui_on_failure, str(e))

    def update_ui_on_success(self, results):
        """Executes safely back on the Main GUI Thread."""
        self.spend_var.set(results["spend"])
        self.sales_var.set(results["sales"])
        self.acos_var.set(results["acos"])
        self.roas_var.set(results["roas"])

        # Populate tables with auto-width adjustment
        self.load_tree(self.top_tree, results["clean_kws"])
        self.load_tree(self.neg_tree, results["neg_kws"])

        self.write_log("Analysis complete! Clean keywords & ASIN subsets segregated with targeting rules.")
        self.write_log("Click 'Download Cleaned Data' to export to multi-sheet Excel.")
        
        # Unlock download button
        self.download_btn.configure(state="normal")
        self.progress.stop()
        messagebox.showinfo("Success", "Analysis Complete! Your cleaned datasets and recommendations are ready.")

    def update_ui_on_failure(self, error_msg):
        self.write_log(f"ERROR: {error_msg}")
        self.progress.stop()
        messagebox.showerror("Error During Processing", f"Pipeline aborted:\n{error_msg}")

    def download_processed_file(self):
        """Allows the user to save the processed, segregated outputs to a clean workbook."""
        if self.df_clean_keywords is None or self.df_raw is None:
            messagebox.showerror("Error", "No analyzed data available to save.")
            return

        default_name = f"Cleaned_{self.raw_file_name.replace('.xlsx', '').replace('.xls', '')}_Report.xlsx"
        save_path = filedialog.asksaveasfilename(
            initialfile=default_name,
            defaultextension=".xlsx",
            filetypes=[("Excel Files", "*.xlsx")]
        )

        if save_path:
            try:
                # Build the multi-sheet output format
                with pd.ExcelWriter(save_path, engine="openpyxl") as writer:
                    self.df_raw.to_excel(writer, sheet_name="Raw_Data", index=False)
                    self.df_clean_keywords.to_excel(writer, sheet_name="Cleaned Keywords", index=False)
                    self.df_asin_placements.to_excel(writer, sheet_name="ASIN Placements", index=False)
                    self.df_neg.to_excel(writer, sheet_name="Negative_Targets", index=False)
                
                self.write_log(f"Cleaned workbook successfully written to: {save_path}")
                messagebox.showinfo("Success", f"Cleaned file downloaded successfully to:\n{os.path.basename(save_path)}")
            except PermissionError:
                messagebox.showerror(
                    "Error", 
                    "Permission Denied: The destination file is currently open in Excel. Please close it and try again."
                )
            except Exception as e:
                messagebox.showerror("Download Error", f"Could not save file:\n{str(e)}")

    def load_tree(self, tree, data):
        """Loads a pandas dataframe into a Tkinter Treeview with auto-fitting column widths."""
        tree.delete(*tree.get_children())

        # Clean string formats to replace underscores with user-friendly headers
        cols = [col.upper().replace("_", " ") for col in data.columns]
        tree["columns"] = list(data.columns)

        for raw_col, clean_col in zip(data.columns, cols):
            tree.heading(raw_col, text=clean_col)
            
            if len(data) > 0:
                max_cell_len = data[raw_col].fillna("").astype(str).map(len).max()
                optimal_width = max(max_cell_len * 9, len(clean_col) * 10, 80)
            else:
                optimal_width = len(clean_col) * 10
                
            tree.column(raw_col, width=min(max(optimal_width, 90), 280), anchor="center")

        # Insert DataFrame rows
        for _, row in data.iterrows():
            formatted_vals = []
            for col_name, val in row.items():
                if pd.isna(val):
                    formatted_vals.append("")
                elif isinstance(val, (int, float)):
                    # Formatting logic for values
                    if col_name in ["CTR", "CVR", "ACoS"]:
                        formatted_vals.append(f"{val * 100:.2f}%" if val <= 1.0 else f"{val:.2f}%")
                    elif col_name in ["Spend", "Sales", "CPC"]:
                        formatted_vals.append(f"${val:,.2f}")
                    elif col_name == "RoAS":
                        formatted_vals.append(f"{val:.2f}")
                    else:
                        formatted_vals.append(f"{val:,.0f}" if val.is_integer() else f"{val:.2f}")
                else:
                    formatted_vals.append(str(val))

            tree.insert("", "end", values=formatted_vals)


if __name__ == "__main__":
    root = tk.Tk()
    app = PPCAnalyzerCombined(root)
    root.mainloop()
