"""
Tkinter-based GUI for the Image-to-PDF Organizer.

This module provides a graphical user interface for selecting,
reordering, and converting images to PDF.
"""

import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from typing import List, Optional, Dict, Any
import threading
from PIL import Image, ImageTk
import sys
from src.services.image_handler import ImageHandler
from src.services.pdf_converter import PDFConverter


class ImageToPdfGUI:
    """Tkinter GUI for the Image-to-PDF Organizer."""
    
    def __init__(self, root: tk.Tk):
        """
        Initialize the GUI.
        
        Args:
            root: The Tkinter root window
        """
        self.root = root
        self.root.title("Image-to-PDF Organizer")
        self.root.geometry("800x600")
        self.root.minsize(700, 500)
        
        # Setup variables
        self.image_paths: List[str] = []
        self.thumbnail_cache: Dict[str, ImageTk.PhotoImage] = {}
        self.page_size = tk.StringVar(value="A4")
        self.compress = tk.BooleanVar(value=False)
        self.quality = tk.IntVar(value=85)
        
        # Configure the grid layout
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # Create main frame
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(1, weight=1)
        
        # Create the UI elements
        self._create_header()
        self._create_image_list()
        self._create_options_panel()
        self._create_status_bar()
        
        # Configure drag and drop
        self._setup_drag_drop()
    
    def _create_header(self) -> None:
        """Create the header with action buttons."""
        header_frame = ttk.Frame(self.main_frame)
        header_frame.grid(column=0, row=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Button(
            header_frame, 
            text="Add Images", 
            command=self._add_images
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(
            header_frame, 
            text="Remove Selected", 
            command=self._remove_selected
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            header_frame, 
            text="Export as PDF", 
            command=self._export_pdf
        ).pack(side=tk.RIGHT, padx=(5, 0))
    
    def _create_image_list(self) -> None:
        """Create the listbox for displaying and reordering images."""
        # Create a frame for the image list and scrollbar
        list_frame = ttk.LabelFrame(self.main_frame, text="Images")
        list_frame.grid(column=0, row=1, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        # Create a frame for the listbox and its scrollbar
        list_inner_frame = ttk.Frame(list_frame)
        list_inner_frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
        list_inner_frame.columnconfigure(0, weight=1)
        list_inner_frame.rowconfigure(0, weight=1)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_inner_frame, orient=tk.VERTICAL)
        scrollbar.grid(column=1, row=0, sticky=(tk.N, tk.S))
        
        # Listbox for images
        self.image_listbox = tk.Listbox(
            list_inner_frame,
            selectmode=tk.SINGLE,
            yscrollcommand=scrollbar.set,
            activestyle='none',
            exportselection=False
        )
        self.image_listbox.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.config(command=self.image_listbox.yview)
        
        # Buttons for reordering images
        reorder_frame = ttk.Frame(list_frame)
        reorder_frame.grid(column=1, row=0, sticky=(tk.N, tk.S), padx=5, pady=5)
        
        ttk.Button(
            reorder_frame, 
            text="▲", 
            width=3,
            command=self._move_up
        ).pack(pady=(0, 5))
        
        ttk.Button(
            reorder_frame, 
            text="▼", 
            width=3,
            command=self._move_down
        ).pack()
        
        # Bind double-click to preview image
        self.image_listbox.bind("<Double-1>", self._preview_image)
    
    def _create_options_panel(self) -> None:
        """Create the panel for PDF options."""
        options_frame = ttk.LabelFrame(self.main_frame, text="PDF Options")
        options_frame.grid(column=0, row=2, sticky=(tk.W, tk.E), pady=(5, 10))
        options_frame.columnconfigure(1, weight=1)
        
        # Page size option
        ttk.Label(options_frame, text="Page Size:").grid(
            column=0, row=0, sticky=tk.W, padx=(10, 5), pady=5
        )
        
        size_combobox = ttk.Combobox(
            options_frame,
            textvariable=self.page_size,
            values=["A4", "LETTER", "LEGAL", "TABLOID", "FIT"],
            state="readonly",
            width=10
        )
        size_combobox.grid(column=1, row=0, sticky=(tk.W), padx=5, pady=5)
        
        # Compression option
        compress_check = ttk.Checkbutton(
            options_frame,
            text="Compress Images",
            variable=self.compress,
            command=self._toggle_compression
        )
        compress_check.grid(column=0, row=1, sticky=tk.W, padx=(10, 5), pady=5)
        
        # Quality slider (initially disabled)
        self.quality_frame = ttk.Frame(options_frame)
        self.quality_frame.grid(column=1, row=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        ttk.Label(self.quality_frame, text="Quality:").pack(side=tk.LEFT)
        
        self.quality_slider = ttk.Scale(
            self.quality_frame,
            from_=1,
            to=100,
            orient=tk.HORIZONTAL,
            variable=self.quality
        )
        self.quality_slider.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        self.quality_label = ttk.Label(self.quality_frame, text="85")
        self.quality_label.pack(side=tk.LEFT, padx=(0, 10))
        
        # Update quality label when slider is moved
        self.quality.trace_add("write", self._update_quality_label)
        
        # Initially disable quality controls
        self._toggle_compression()
    
    def _create_status_bar(self) -> None:
        """Create the status bar with progress indicator."""
        status_frame = ttk.Frame(self.main_frame)
        status_frame.grid(column=0, row=3, sticky=(tk.W, tk.E))
        status_frame.columnconfigure(0, weight=1)
        
        # Progress bar
        self.progress_var = tk.DoubleVar(value=0.0)
        self.progress_bar = ttk.Progressbar(
            status_frame,
            variable=self.progress_var,
            mode="determinate"
        )
        self.progress_bar.grid(column=0, row=0, sticky=(tk.W, tk.E), pady=(5, 0))
        
        # Status label
        self.status_var = tk.StringVar(value="Ready")
        status_label = ttk.Label(
            status_frame,
            textvariable=self.status_var,
            anchor=tk.W
        )
        status_label.grid(column=0, row=1, sticky=(tk.W, tk.E), pady=(5, 0))
    
    def _setup_drag_drop(self) -> None:
        """
        Configure drag and drop functionality.
        
        Note: This is a placeholder for drag and drop functionality.
        Standard Tkinter doesn't support drag and drop natively.
        To implement it, we would need to install additional packages like tkinterdnd2.
        """
        # Add a label explaining drag and drop is not available
        drop_label = ttk.Label(
            self.main_frame,
            text="Tip: You can add multiple files at once using the 'Add Images' button.",
            font=('', 9, 'italic')
        )
        drop_label.grid(column=0, row=4, sticky=(tk.W), pady=(5, 0))
    
    def _handle_drop(self, event=None) -> None:
        """
        Handle files dropped onto the listbox.
        This is a placeholder for future implementation with tkinterdnd2 or similar.
        
        Args:
            event: The drop event (optional)
        """
        # This method is kept as a placeholder for future drag and drop implementation
        pass
    
    def _add_images(self) -> None:
        """Open a file dialog to select and add images."""
        filetypes = [
            ("Image Files", "*.jpg *.jpeg *.png *.bmp *.tiff *.gif"),
            ("All Files", "*.*")
        ]
        
        paths = filedialog.askopenfilenames(
            title="Select Image Files",
            filetypes=filetypes
        )
        
        if paths:  # If user didn't cancel
            self._add_images_from_paths(paths)
    
    def _add_images_from_paths(self, paths: List[str]) -> None:
        """
        Add images from a list of file paths.
        
        Args:
            paths: List of image file paths
        """
        added_count = 0
        
        for path in paths:
            if not os.path.exists(path):
                continue
                
            if not ImageHandler.is_valid_image(path):
                continue
                
            # Add to our list and listbox
            self.image_paths.append(path)
            filename = os.path.basename(path)
            self.image_listbox.insert(tk.END, filename)
            added_count += 1
        
        if added_count > 0:
            self.status_var.set(f"Added {added_count} images")
        else:
            self.status_var.set("No valid images were added")
    
    def _remove_selected(self) -> None:
        """Remove the selected image from the list."""
        selected = self.image_listbox.curselection()
        
        if not selected:
            return
            
        index = selected[0]
        
        # Remove from our data
        del self.image_paths[index]
        
        # Remove from listbox
        self.image_listbox.delete(index)
        
        # Update status
        self.status_var.set("Image removed")
    
    def _move_up(self) -> None:
        """Move the selected image up in the list."""
        selected = self.image_listbox.curselection()
        
        if not selected or selected[0] == 0:
            return
            
        index = selected[0]
        
        # Swap in our data list
        self.image_paths[index], self.image_paths[index-1] = \
            self.image_paths[index-1], self.image_paths[index]
        
        # Update listbox
        filename = self.image_listbox.get(index)
        self.image_listbox.delete(index)
        self.image_listbox.insert(index-1, filename)
        self.image_listbox.selection_set(index-1)
    
    def _move_down(self) -> None:
        """Move the selected image down in the list."""
        selected = self.image_listbox.curselection()
        
        if not selected or selected[0] == len(self.image_paths) - 1:
            return
            
        index = selected[0]
        
        # Swap in our data list
        self.image_paths[index], self.image_paths[index+1] = \
            self.image_paths[index+1], self.image_paths[index]
        
        # Update listbox
        filename = self.image_listbox.get(index)
        self.image_listbox.delete(index)
        self.image_listbox.insert(index+1, filename)
        self.image_listbox.selection_set(index+1)
    
    def _preview_image(self, event=None) -> None:
        """
        Show a preview of the selected image.
        
        Args:
            event: The event that triggered this action (optional)
        """
        selected = self.image_listbox.curselection()
        
        if not selected:
            return
            
        index = selected[0]
        image_path = self.image_paths[index]
        
        # Create a new top-level window for the preview
        preview_window = tk.Toplevel(self.root)
        preview_window.title(f"Preview: {os.path.basename(image_path)}")
        preview_window.geometry("800x600")
        
        # Make the window modal
        preview_window.transient(self.root)
        preview_window.grab_set()
        
        try:
            # Open and resize the image for preview
            with Image.open(image_path) as img:
                # Resize image to fit in the window while maintaining aspect ratio
                img.thumbnail((780, 580))
                photo = ImageTk.PhotoImage(img)
                
                # Create a label to display the image
                label = ttk.Label(preview_window, image=photo)
                label.image = photo  # Keep a reference to prevent garbage collection
                label.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
                
                # Add a close button
                ttk.Button(
                    preview_window, 
                    text="Close", 
                    command=preview_window.destroy
                ).pack(pady=10)
        
        except Exception as e:
            messagebox.showerror("Error", f"Could not preview image: {e}")
            preview_window.destroy()
    
    def _toggle_compression(self) -> None:
        """Enable or disable the quality slider based on compression checkbox."""
        for widget in self.quality_frame.winfo_children():
            if self.compress.get():
                widget.configure(state=tk.NORMAL)
            else:
                widget.configure(state=tk.DISABLED)
    
    def _update_quality_label(self, *args) -> None:
        """Update the quality label when the slider is moved."""
        self.quality_label.config(text=str(self.quality.get()))
    
    def _export_pdf(self) -> None:
        """Open a save dialog and export images to PDF."""
        if not self.image_paths:
            messagebox.showwarning(
                "No Images", 
                "Please add at least one image before exporting."
            )
            return
        
        # Ask for save location
        output_path = filedialog.asksaveasfilename(
            title="Save PDF As",
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf"), ("All Files", "*.*")]
        )
        
        if not output_path:  # User cancelled
            return
        
        # Disable UI during export
        self._set_ui_state(tk.DISABLED)
        self.progress_var.set(0.0)
        self.status_var.set("Exporting PDF...")
        
        # Create a callback for progress updates
        def progress_callback(progress: float) -> None:
            self.progress_var.set(progress)
            self.root.update_idletasks()  # Force UI update
        
        # Run the conversion in a separate thread to keep UI responsive
        def export_thread() -> None:
            try:
                converter = PDFConverter()
                converter.convert_images_to_pdf(
                    image_paths=self.image_paths,
                    output_path=output_path,
                    page_size=self.page_size.get(),
                    compress=self.compress.get(),
                    compression_quality=self.quality.get(),
                    callback=progress_callback
                )
                
                # Show success message in the main thread
                self.root.after(
                    0, 
                    lambda: self._export_complete(output_path)
                )
            
            except Exception as exception_instance:
                # Show error message in the main thread
                error_message = str(exception_instance)
                self.root.after(
                    0, 
                    lambda: self._export_error(error_message)
                )
        
        # Start the export thread
        threading.Thread(target=export_thread, daemon=True).start()
    
    def _export_complete(self, output_path: str) -> None:
        """
        Handle successful PDF export.
        
        Args:
            output_path: Path to the exported PDF
        """
        self._set_ui_state(tk.NORMAL)
        self.progress_var.set(1.0)
        self.status_var.set(f"PDF exported successfully: {os.path.basename(output_path)}")
        
        # Show success message with option to open the PDF
        if messagebox.askyesno(
            "Export Complete",
            f"PDF exported successfully to:\n{output_path}\n\nWould you like to open it now?"
        ):
            self._open_pdf(output_path)
    
    def _export_error(self, error_message: str) -> None:
        """
        Handle PDF export error.
        
        Args:
            error_message: The error message to display
        """
        self._set_ui_state(tk.NORMAL)
        self.progress_var.set(0.0)
        self.status_var.set("Export failed")
        
        messagebox.showerror(
            "Export Error",
            f"Failed to export PDF: {error_message}"
        )
    
    def _set_ui_state(self, state: str) -> None:
        """
        Enable or disable UI elements.
        
        Args:
            state: The state to set (tk.NORMAL or tk.DISABLED)
        """
        # Update all interactive elements
        for widget in self.main_frame.winfo_children():
            if isinstance(widget, (ttk.Button, ttk.Combobox, ttk.Checkbutton, ttk.Entry)):
                widget.configure(state=state)
            
            # Also update child widgets if it's a container
            if hasattr(widget, 'winfo_children'):
                for child in widget.winfo_children():
                    if isinstance(child, (ttk.Button, ttk.Combobox, ttk.Checkbutton, ttk.Entry)):
                        child.configure(state=state)
        
        # The listbox is a special case (it's a tk widget, not ttk)
        self.image_listbox.configure(state=state)
    
    def _open_pdf(self, path: str) -> None:
        """
        Open the PDF with the default system viewer.
        
        Args:
            path: Path to the PDF file
        """
        import platform
        import subprocess
        
        try:
            if platform.system() == 'Windows':
                os.startfile(path)
            elif platform.system() == 'Darwin':  # macOS
                subprocess.call(['open', path])
            else:  # Linux
                subprocess.call(['xdg-open', path])
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Could not open PDF: {e}"
            )


def main():
    """Run the GUI application."""
    root = tk.Tk()
    app = ImageToPdfGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
