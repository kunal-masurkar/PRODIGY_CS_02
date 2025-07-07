import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os

# Encryption/Decryption functions
def encrypt_image(img, key):
    encrypted = img.copy()
    pixels = encrypted.load()
    for i in range(encrypted.width):
        for j in range(encrypted.height):
            r, g, b = pixels[i, j][:3]
            pixels[i, j] = ((r + key) % 256, (g + key) % 256, (b + key) % 256)
    return encrypted

def decrypt_image(img, key):
    decrypted = img.copy()
    pixels = decrypted.load()
    for i in range(decrypted.width):
        for j in range(decrypted.height):
            r, g, b = pixels[i, j][:3]
            pixels[i, j] = ((r - key) % 256, (g - key) % 256, (b - key) % 256)
    return decrypted

class ImageCipherApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Pixel-based Image Encryption Tool')
        self.root.geometry('700x500')
        self.image = None
        self.processed_image = None
        self.img_label = None
        self.tk_img = None
        self.tk_proc_img = None

        self.setup_ui()

    def setup_ui(self):
        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        btn_upload = tk.Button(frame, text='Upload Image', command=self.upload_image)
        btn_upload.grid(row=0, column=0, padx=5)

        tk.Label(frame, text='Key:').grid(row=0, column=1)
        self.key_entry = tk.Entry(frame, width=5)
        self.key_entry.grid(row=0, column=2, padx=5)
        self.key_entry.insert(0, '10')

        btn_encrypt = tk.Button(frame, text='Encrypt', command=self.encrypt)
        btn_encrypt.grid(row=0, column=3, padx=5)
        btn_decrypt = tk.Button(frame, text='Decrypt', command=self.decrypt)
        btn_decrypt.grid(row=0, column=4, padx=5)
        btn_save = tk.Button(frame, text='Save Image', command=self.save_image)
        btn_save.grid(row=0, column=5, padx=5)

        self.img_panel = tk.Label(self.root, text='Original Image will appear here')
        self.img_panel.pack(side=tk.LEFT, padx=10, pady=10, expand=True)
        self.proc_img_panel = tk.Label(self.root, text='Processed Image will appear here')
        self.proc_img_panel.pack(side=tk.RIGHT, padx=10, pady=10, expand=True)

    def upload_image(self):
        file_path = filedialog.askopenfilename(filetypes=[('Image Files', '*.png;*.jpg;*.jpeg;*.bmp')])
        if file_path:
            self.image = Image.open(file_path).convert('RGB')
            self.display_image(self.image, self.img_panel)
            self.processed_image = None
            self.proc_img_panel.config(image='', text='Processed Image will appear here')

    def display_image(self, img, panel):
        img_resized = img.copy()
        img_resized.thumbnail((300, 300))
        tk_img = ImageTk.PhotoImage(img_resized)
        panel.config(image=tk_img, text='')
        panel.image = tk_img  # Keep reference

    def get_key(self):
        try:
            return int(self.key_entry.get())
        except ValueError:
            messagebox.showerror('Error', 'Key must be an integer.')
            return None

    def encrypt(self):
        key = self.get_key()
        if self.image and key is not None:
            self.processed_image = encrypt_image(self.image, key)
            self.display_image(self.processed_image, self.proc_img_panel)
        else:
            messagebox.showwarning('Warning', 'Please upload an image and enter a valid key.')

    def decrypt(self):
        key = self.get_key()
        if self.image and key is not None:
            self.processed_image = decrypt_image(self.image, key)
            self.display_image(self.processed_image, self.proc_img_panel)
        else:
            messagebox.showwarning('Warning', 'Please upload an image and enter a valid key.')

    def save_image(self):
        if self.processed_image:
            file_path = filedialog.asksaveasfilename(defaultextension='.png', filetypes=[('PNG Image', '*.png')])
            if file_path:
                self.processed_image.save(file_path)
                messagebox.showinfo('Saved', f'Image saved to {file_path}')
        else:
            messagebox.showwarning('Warning', 'No processed image to save.')

if __name__ == '__main__':
    root = tk.Tk()
    app = ImageCipherApp(root)
    root.mainloop() 
