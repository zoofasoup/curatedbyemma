import numpy as np
from PIL import Image, ImageFilter, ImageEnhance
import os
import sys

def de_ai_process(image_path: str, output_path: str):
    """
    Transforms an AI portrait into an authentic 35mm / candid camera photo:
    1. Removes hyper-smooth plastic sheen with organic multi-scale grain
    2. Applies analog film tone curve (lifts harsh digital blacks, softens digital clip)
    3. Lowers digital over-saturation and warms skin tones naturally
    4. Applies subtle lens diffusion
    """
    print(f"Processing: {image_path} -> {output_path}")
    img = Image.open(image_path).convert("RGB")
    w, h = img.size

    # Step 1: Subtle lens softening (takes away the razor-sharp CGI vector look)
    softened = img.filter(ImageFilter.GaussianBlur(radius=0.4))
    
    # Step 2: Convert to NumPy float array (0.0 to 1.0)
    arr = np.array(softened, dtype=np.float32) / 255.0

    # Step 3: Kodak Portra Tone Curve (Lifts digital blacks & softens blown highlights)
    # Lift blacks from 0.0 to ~0.04 (film negative characteristic)
    lift = 0.035
    arr = lift + arr * (1.0 - lift)
    # Gentle S-curve softening (reduces harsh digital contrast)
    arr = np.clip(arr, 0.0, 1.0)
    arr = arr ** 0.98

    # Step 4: Subtle warm color balance (less cold/synthetic)
    # Slightly enhance red/yellow midtones (+1.5% red, +0.5% green, -1% blue)
    arr[:, :, 0] = np.clip(arr[:, :, 0] * 1.018, 0, 1)
    arr[:, :, 1] = np.clip(arr[:, :, 1] * 1.006, 0, 1)
    arr[:, :, 2] = np.clip(arr[:, :, 2] * 0.982, 0, 1)

    # Step 5: Multi-scale Organic 35mm Film Grain
    # Real film grain lives heavily in the midtones (skin), less in extreme blacks and pure whites
    luminance = 0.299 * arr[:, :, 0] + 0.587 * arr[:, :, 1] + 0.114 * arr[:, :, 2]
    # Midtone mask: parabolic curve peaking around 0.5
    midtone_mask = 4.0 * luminance * (1.0 - luminance)
    midtone_mask = np.clip(midtone_mask, 0.15, 1.0)

    # Fine grain
    np.random.seed(42) # Consistent realistic noise pattern
    fine_grain = np.random.normal(0.0, 0.024, (h, w, 1))
    
    # Coarser film clump grain
    coarse_raw = np.random.normal(0.0, 0.015, (h // 2, w // 2, 1))
    coarse_img = Image.fromarray(((coarse_raw[:, :, 0] + 0.5) * 255).astype(np.uint8), mode='L')
    coarse_resized = coarse_img.resize((w, h), Image.Resampling.BICUBIC)
    coarse_grain = (np.array(coarse_resized, dtype=np.float32) / 255.0 - 0.5)[:, :, np.newaxis]

    # Combine grain weighted by midtone mask
    total_grain = (fine_grain * 0.65 + coarse_grain * 0.35) * midtone_mask[:, :, np.newaxis]
    arr = np.clip(arr + total_grain, 0.0, 1.0)

    # Step 6: Convert back to PIL Image
    final_img = Image.fromarray((arr * 255.0).astype(np.uint8))

    # Step 7: Slightly tame digital saturation (-6%)
    converter = ImageEnhance.Color(final_img)
    final_img = converter.enhance(0.94)

    # Save with high quality JPEG
    final_img.save(output_path, "JPEG", quality=95, subsampling=0)
    print(f"✓ Saved authentic film texture photo to {output_path}!")

if __name__ == "__main__":
    assets_dir = "/Users/macbookair/.gemini/antigravity/scratch/affiliate-engine/public/assets/emma"
    files = ["emma_desk.jpg", "emma_couch.jpg", "emma_cafe.jpg", "emma_kitchen.jpg"]
    
    for f in files:
        src = os.path.join(assets_dir, f)
        if os.path.exists(src):
            # Backup original
            orig_backup = src.replace(".jpg", "_raw_ai.jpg")
            if not os.path.exists(orig_backup):
                os.system(f"cp {src} {orig_backup}")
            de_ai_process(orig_backup, src)
