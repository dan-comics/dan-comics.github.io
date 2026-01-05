# How to Add New Comics or Series

Your website now **automatically updates** when you add new folders or images! No code changes needed.

## 📚 Adding a New Comic to an Existing Series

1. Navigate to the series folder in `Website/[Series Name]/`
2. Add your comic image files (.jpeg, .jpg, .png, .gif, or .pdf)
3. Commit and push to GitHub:
   ```bash
   git add .
   git commit -m "Add new comics to [Series Name]"
   git push
   ```
4. Wait 2-3 minutes for GitHub Pages to rebuild
5. Refresh your website - the new comics will appear automatically! ✨

## 🆕 Adding a New Series (Folder)

1. Create a new folder in `Website/` with your series name
2. Add comic images to that folder
3. Commit and push to GitHub:
   ```bash
   git add .
   git commit -m "Add new series: [Series Name]"
   git push
   ```
4. The new series will appear with a default 📚 icon and random color

### Optional: Customize New Series Icon & Color

To give your new series a custom icon and color:

1. Open `index.html` in a text editor
2. Find the `seriesConfig` section (around line 545)
3. Add your series like this:
   ```javascript
   'Your Series Name': { icon: '🎨', color: '#FF5733' }
   ```
4. Commit and push the change

**Example:**
```javascript
const seriesConfig = {
    'Origional Dan': { icon: '⭐', color: '#FF6B6B' },
    'Dan Funnies': { icon: '😂', color: '#4ECDC4' },
    'My New Series': { icon: '🚀', color: '#42A5F5' }  // ← Add your new series here
};
```

## 📝 Supported File Types

- `.jpeg` / `.jpg`
- `.png`
- `.gif`
- `.pdf`

## ⚙️ How It Works

The website uses GitHub's API to:
- Automatically discover all folders in `Website/`
- Find all image/PDF files in each folder
- Display them without manual configuration

No more updating JavaScript arrays manually! 🎉

## 🔧 Troubleshooting

**Comics not showing up?**
1. Wait 2-3 minutes after pushing to GitHub
2. Clear your browser cache and refresh
3. Check the browser console (F12) for errors
4. Make sure files are in the `Website/` folder, not the root

**New series not appearing?**
1. Make sure the folder is inside `Website/`
2. Add at least one image file to the folder
3. Check that filenames don't have special characters that might cause issues
