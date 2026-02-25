# Sorcery TCG Cards Database - Scripts

This folder contains automation scripts for maintaining the card image database.

## 📝 Scripts

### `generate_thumbnails.py`

Automatically generates JPG thumbnails from PNG card images.

**What it does:**
- Recursively scans `data/imgs/full/` for all PNG files
- Creates corresponding JPG thumbnails in `data/imgs/thumbs/`
- Preserves the exact folder structure (set/product/filename)
- Only regenerates thumbnails that are outdated or missing
- Works with **any set name and product type** automatically

**Configuration:**
- Thumbnail width: 300px (height scales proportionally)
- JPEG quality: 85%
- Format: PNG → JPG conversion with white background

**Usage:**

```bash
# Run from repository root
python scripts/generate_thumbnails.py
```

**Requirements:**
- Python 3.7+
- Pillow library (`pip install Pillow`)

**Example output:**
```
Found 2500 PNG images
Thumbnail size: 300px width
JPEG quality: 85%

✨ Created thumbnail 50/2500: Gothic/b_f/zombie_bruiser_b_f.jpg
✨ Created thumbnail 100/2500: Promotional/ai_f/skeleton_ai_f.jpg
...

Summary:
  ✅ Processed: 450
     - Created: 450
     - Updated: 0
  ⏭️  Skipped (up-to-date): 2050
  ❌ Errors: 0
  📊 Total images: 2500
```

---

### `update_cards_db.py`

Fetches card data from the official Sorcery API and updates `data/db/cards.json`.

**What it does:**
- Fetches all cards from `https://api.sorcerytcg.com/api/cards`
- Normalizes variant slugs (hyphens → underscores) for compatibility with image filenames
- Overwrites `data/db/cards.json` with the latest data (including new expansions)

**Usage:**

```bash
# Run from repository root
python scripts/update_cards_db.py
```

**Requirements:**
- Python 3.7+
- `requests` (recommended): `pip install requests` — or use built-in `urllib` (slower, may have SSL issues on some systems)

**Example output:**
```
============================================================
Sorcery TCG – Update Cards Database
============================================================

Fetching cards from API...
  Retrieved 1234 cards
Normalizing slugs for image compatibility...
Writing to data/db/cards.json...

Database updated successfully.
```

---

## 🤖 GitHub Actions

The thumbnail generation runs automatically via GitHub Actions when:
- PNG images are pushed to `data/imgs/full/**`
- Manual trigger via "Actions" tab → "Generate Card Thumbnails" → "Run workflow"

See `.github/workflows/generate-thumbnails.yml` for details.

---

## 🆕 Adding New Sets or Product Types

The script is **fully automatic** and doesn't require configuration when adding:
- New sets (e.g., Gothic, Promotional)
- New product types (e.g., ai, tc, op, du)
- New card images

Just add the PNG files to the correct folder structure:
```
data/imgs/full/<SetName>/<product>_<finish>/<cardname>_<product>_<finish>.png
```

The script will automatically:
1. Detect the new images
2. Create the matching folder structure in `thumbs/`
3. Generate the thumbnails

---

## 🔧 Manual Testing

To test thumbnail generation locally:

```bash
# Install dependencies
pip install Pillow

# Run the script
python scripts/generate_thumbnails.py

# Check the output in data/imgs/thumbs/
```

