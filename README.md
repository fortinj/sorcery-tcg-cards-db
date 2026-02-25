Updated card images database for Sorcery Contested Realms TCG

All the images here are downloaded from their official shared drive:
https://drive.google.com/drive/folders/17IrJkRGmIU9fDSTU2JQEU9JlFzb5liLJ

## Updating the database for new expansions

1. **Update card data** (metadata, new sets, errata):
   ```bash
   pip install -r requirements.txt  # or: pip install requests
   python scripts/update_cards_db.py
   ```

2. **Download new images** from the Google Drive and place them in `data/imgs/full/<SetName>/<product>_<finish>/`.

3. **Generate thumbnails**:
   ```bash
   pip install Pillow
   python scripts/generate_thumbnails.py
   ```
