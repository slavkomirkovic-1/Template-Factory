from tkinter import filedialog, messagebox
from os.path import exists, dirname
from os import makedirs

import customtkinter as ctk
import json


class TemplateFactory(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configure window
        self.title("Template Factory")
        self.geometry("800x600")
        self.minsize(800, 600)
        
        # Set the theme
        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("blue")
        
        # Configure grid layout (2x1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Create left panel
        self.left_panel = ctk.CTkFrame(self, corner_radius=10)
        self.left_panel.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        # Configure left panel grid
        self.left_panel.grid_rowconfigure(2, weight=1)
        self.left_panel.grid_columnconfigure(0, weight=1)

        # Left panel elements
        self.title_label = ctk.CTkLabel(
            self.left_panel, 
            text="Template Factory",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.title_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.templates_label = ctk.CTkLabel(
            self.left_panel,
            text="Template Details",
            font=ctk.CTkFont(size=16)
        )
        self.templates_label.grid(row=1, column=0, padx=20, pady=(10, 0), sticky="w")

        self.templates_list = ctk.CTkTextbox(
            self.left_panel,
            font=ctk.CTkFont(size=13),
            activate_scrollbars=True
        )
        self.templates_list.grid(row=2, column=0, padx=20, pady=(10, 10), sticky="nsew")
        self.templates_list.configure(state="disabled")  # Make it read-only

        self.load_templates_btn = ctk.CTkButton(
            self.left_panel,
            text="Load Templates",
            command=self.load_templates,
            height=40
        )
        self.load_templates_btn.grid(row=3, column=0, padx=20, pady=(0, 20), sticky="ew")

        # Create right panel
        self.right_panel = ctk.CTkFrame(self, corner_radius=10)
        self.right_panel.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        # Configure right panel grid
        self.right_panel.grid_rowconfigure(4, weight=1)
        self.right_panel.grid_columnconfigure(0, weight=1)

        # Right panel elements
        self.project_name_label = ctk.CTkLabel(
            self.right_panel,
            text="Project Name",
            font=ctk.CTkFont(size=16)
        )
        self.project_name_label.grid(row=0, column=0, padx=20, pady=(20, 0), sticky="w")
        
        self.project_name_entry = ctk.CTkEntry(
            self.right_panel,
            height=40,
            placeholder_text="Enter project name..."
        )
        self.project_name_entry.grid(row=1, column=0, padx=20, pady=(10, 20), sticky="ew")

        self.template_name_label = ctk.CTkLabel(
            self.right_panel,
            text="Select Template",
            font=ctk.CTkFont(size=16)
        )
        self.template_name_label.grid(row=2, column=0, padx=20, pady=(10, 0), sticky="w")
        
        self.template_selector = ctk.CTkComboBox(
            self.right_panel,
            height=40,
            state="readonly",
            values=[],
            command=self.on_template_selected
        )
        self.template_selector.grid(row=3, column=0, padx=20, pady=(10, 20), sticky="ew")

        self.create_project_btn = ctk.CTkButton(
            self.right_panel,
            text="Create Project",
            command=self.create_project,
            height=40
        )
        self.create_project_btn.grid(row=5, column=0, padx=20, pady=(0, 20), sticky="ew")

        # Initialize variables
        self.templates = None
        self.templates_file_path = None
        self.current_template = None

    def on_template_selected(self, choice):
        if not self.templates:
            return

        # Find the selected template
        for template in self.templates:
            if template['templateName'] == choice:
                self.current_template = template
                # Update template details in the left panel
                self.templates_list.configure(state="normal")
                self.templates_list.delete("0.0", "end")
                
                # Display template details
                details = f"Template: {template['templateName']}\n\n"
                details += f"Description:\n{template['templateDescription']}\n\n"
                details += "Files to be created:\n"
                for file in template['TemplateFiles']:
                    details += f"• {file['name']}\n"
                
                self.templates_list.insert("0.0", details)
                self.templates_list.configure(state="disabled")
                break

    def load_templates(self):
        self.templates_file_path = filedialog.askopenfilename(
            title="Select Templates File",
            filetypes=[("JSON files", "*.json")]
        )
        
        if self.templates_file_path:
            try:
                with open(self.templates_file_path) as f:
                    self.templates = json.load(f)
                
                # Update template selector
                template_names = [t['templateName'] for t in self.templates]
                self.template_selector.configure(values=template_names)
                if template_names:
                    self.template_selector.set(template_names[0])
                    self.on_template_selected(template_names[0])
                
            except Exception as e:
                messagebox.showerror("Error", f"Error loading templates: {e}")

    def create_project(self):
        if not self.templates:
            messagebox.showwarning("Warning", "Please load templates first")
            return

        project_name = self.project_name_entry.get().strip()
        if not project_name:
            messagebox.showwarning("Warning", "Please enter a project name")
            return

        if not self.current_template:
            messagebox.showwarning("Warning", "Please select a template")
            return

        try:
            # Create the project root directory
            if not exists(project_name):
                makedirs(project_name)

            # Create files from template
            for file_info in self.current_template['TemplateFiles']:
                file_path = f'{project_name}/{file_info["name"]}'
                dir_path = dirname(file_path)
                if dir_path and not exists(dir_path):
                    makedirs(dir_path)
                
                with open(file_path, 'w') as f:
                    f.write(file_info['content'])

            messagebox.showinfo("Success", f"Project '{project_name}' created successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error creating project: {e}")

if __name__ == "__main__":
    app = TemplateFactory()
    app.mainloop()