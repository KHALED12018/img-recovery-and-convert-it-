import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import os

class RecoilConverterApp:
    def __init__(self, master):
        self.master = master
        master.title("Recoil to PNG Converter")
        master.geometry("500x600")
        master.resizable(False, False)

        self.style = ttk.Style()
        self.style.configure("TButton", padding=6, relief="flat", background="#ccc")
        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure("TLabel", background="#f0f0f0", font=("Helvetica", 12))
        self.style.configure("Treeview", font=("Helvetica", 10))

        self.frame = ttk.Frame(master, padding="10")
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.entry_file_path = ttk.Entry(self.frame, width=50)
        self.entry_file_path.grid(row=0, column=0, padx=10, pady=10)

        self.browse_button = ttk.Button(self.frame, text="Browse", command=self.browse_file)
        self.browse_button.grid(row=0, column=1, padx=10, pady=10)

        self.file_info_tree = ttk.Treeview(self.frame, columns=("Attribute", "Value"), show="headings")
        self.file_info_tree.heading("Attribute", text="Attribute")
        self.file_info_tree.heading("Value", text="Value")
        self.file_info_tree.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        self.convert_button = ttk.Button(self.frame, text="Convert to PNG", command=self.convert_and_display)
        self.convert_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        self.reset_button = ttk.Button(self.frame, text="Reset", command=self.reset_file)
        self.reset_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)
        self.reset_button.config(state=tk.DISABLED)  # يتم تعطيله حتى يتم تحويل ملف بنجاح

        self.img_frame = ttk.Frame(self.frame, width=300, height=300, relief="sunken", style="TFrame")
        self.img_frame.grid(row=4, column=0, columnspan=2, padx=10, pady=10)
        self.img_frame.grid_propagate(False)

        self.img_label = ttk.Label(self.img_frame, style="TLabel")
        self.img_label.pack(expand=True)

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Binary files", "*.bin")])
        if file_path:
            self.entry_file_path.delete(0, tk.END)
            self.entry_file_path.insert(0, file_path)
            self.update_file_info(file_path)

    def update_file_info(self, file_path):
        self.file_info_tree.delete(*self.file_info_tree.get_children())
        file_size = os.path.getsize(file_path)
        self.file_info_tree.insert("", "end", values=("File Size", f"{file_size} bytes"))
        # Add more file info if needed

    def convert_and_display(self):
        recoil_file = self.entry_file_path.get()
        if not recoil_file or not os.path.exists(recoil_file):
            messagebox.showwarning("File Not Found", "Please select a valid Recoil file.")
            return

        try:
            width, height = 640, 400  # الأبعاد الافتراضية للصورة

            with open(recoil_file, "rb") as f:
                image_data = f.read()

            image = Image.frombytes('P', (width, height), image_data)

            # يجب تعديل هذا الجزء لتحديد لوحة الألوان الصحيحة (Palette)
            palette = [
                0x00, 0x00, 0x00,  # أسود
                0x68, 0x01, 0x00,  # لون 1
                0x89, 0x19, 0x7b,  # لون 2
                # أضف بقية الألوان من لوحة الألوان هنا...
            ]
            image.putpalette(palette * 16)

            png_file = recoil_file.replace(".bin", ".png")
            image.save(png_file)

            self.display_image(png_file)
            self.reset_button.config(state=tk.NORMAL)

            messagebox.showinfo("Conversion Successful", "File converted and saved successfully.")

        except Exception as e:
            messagebox.showerror("Conversion Error", f"Failed to convert {recoil_file} to PNG: {e}")

    def display_image(self, png_file):
        img = Image.open(png_file)
        img.thumbnail((300, 300))  # تغيير حجم الصورة لتناسب الإطار
        img = ImageTk.PhotoImage(img)
        self.img_label.config(image=img)
        self.img_label.image = img  # الاحتفاظ بمرجع لتجنب جمع القمامة

    def reset_file(self):
        recoil_file = self.entry_file_path.get()
        if not recoil_file or not os.path.exists(recoil_file):
            return

        original_file = recoil_file.replace(".bin", "_original.bin")
        try:
            os.rename(recoil_file, original_file)
            self.entry_file_path.delete(0, tk.END)
            self.file_info_tree.delete(*self.file_info_tree.get_children())
            self.img_label.config(image=None)
            self.reset_button.config(state=tk.DISABLED)

            messagebox.showinfo("File Reset", "Original file restored successfully.")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to reset file: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = RecoilConverterApp(root)
    root.mainloop()

