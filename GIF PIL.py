from PIL import Image
from tkinter import filedialog, messagebox
import tkinter as tk
import os
from pathlib import Path
import time

def create_output_directory(base_dir: str) -> Path:
    """Create and return output directory path with timestamp"""
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    output_dir = Path(base_dir) / f"gif_frames_{timestamp}"
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir

def extract_gif_frames(gif_path: str, output_dir: Path) -> int:
    """Extract frames from GIF and save as PNG files"""
    with Image.open(gif_path) as gif:
        # Get total number of frames
        total_frames = 0
        try:
            while True:
                gif.seek(total_frames)
                total_frames += 1
        except EOFError:
            pass
        
        # Reset to first frame
        gif.seek(0)
        
        # Extract frames with progress tracking
        for frame_num in range(total_frames):
            # Convert to RGBA to ensure consistency
            current_frame = gif.convert('RGBA')
            frame_filename = output_dir / f"frame_{frame_num:04d}.png"
            current_frame.save(frame_filename, "PNG", optimize=True)
            
            # Display progress
            progress = (frame_num + 1) / total_frames * 100
            print(f"Progress: {progress:.1f}% - Saved {frame_filename.name}")
            
            # Move to next frame if not at end
            if frame_num < total_frames - 1:
                gif.seek(frame_num + 1)
                
        return total_frames

def main():
    # Create and hide the tkinter root window
    root = tk.Tk()
    root.withdraw()

    try:
        # Open file dialog to select GIF file
        print("Please select a GIF file...")
        gif_path = filedialog.askopenfilename(
            title="Select a GIF file",
            filetypes=[("GIF files", "*.gif"), ("All files", "*.*")]
        )

        if not gif_path:
            print("No file selected. Exiting...")
            return

        # Create output directory with timestamp
        output_dir = create_output_directory("gif_frames")
        
        # Record start time
        start_time = time.time()
        
        # Process the GIF file
        with Image.open(gif_path) as im:
            print("\nGIF Information:")
            print(f"Format: {im.format}")
            print(f"Size: {im.size[0]}x{im.size[1]} pixels")
            print(f"Mode: {im.mode}")
            print(f"Input file: {Path(gif_path).name}")
            print(f"Output directory: {output_dir}\n")

        # Extract frames
        total_frames = extract_gif_frames(gif_path, output_dir)
        
        # Calculate and display processing time
        elapsed_time = time.time() - start_time
        print(f"\nExtraction Complete!")
        print(f"Total frames extracted: {total_frames}")
        print(f"Processing time: {elapsed_time:.2f} seconds")
        print(f"Average time per frame: {(elapsed_time/total_frames):.3f} seconds")
        print(f"Files saved to: {output_dir}")
        
        # Show completion message
        messagebox.showinfo("Success", 
            f"Successfully extracted {total_frames} frames\nSaved to: {output_dir}")

    except FileNotFoundError:
        messagebox.showerror("Error", "File not found. Please check the file path.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred:\n{str(e)}")
    finally:
        root.destroy()

if __name__ == "__main__":
    main()
