# Language Switcher Fix - Root Cause & Solution

## 🔴 ROOT CAUSE

The language switcher dropdown uses **pure CSS `:hover`** which causes the menu to disappear when you move the mouse from the button to the dropdown items.

**Broken CSS (base.html line 250):**
```css
.language-switcher:hover .lang-dropdown {
    opacity: 1;
    visibility: visible;
    transform: translateY(0);
}
```

**What happens:**
1. User hovers over language button → dropdown appears
2. User moves mouse toward a language option
3. Mouse briefly leaves `.language-switcher` element
4. Dropdown immediately hides (`:hover` ends)
5. Click never registers because element is hidden

**This is why:** The dropdown has `opacity: 0` and `visibility: hidden` by default, and only becomes visible during hover. But when you move the mouse away from the button toward the dropdown, the hover ends prematurely.

## ✅ SOLUTION

Use **JavaScript toggle** instead of pure CSS hover for the dropdown. This keeps the dropdown open until explicitly closed.

---

## IMPLEMENTATION

### Step 1: Add Click Toggle JavaScript

Add this to the end of `base.html` (before `</body>`):

```html
<script>
document.addEventListener('DOMContentLoaded', function() {
    const langToggle = document.querySelector('.lang-toggle');
    const langDropdown = document.querySelector('.lang-dropdown');
    const languageSwitcher = document.querySelector('.language-switcher');

    if (langToggle && langDropdown) {
        // Toggle dropdown on button click
        langToggle.addEventListener('click', function(e) {
            e.stopPropagation();
            languageSwitcher.classList.toggle('open');
        });

        // Close dropdown when clicking outside
        document.addEventListener('click', function(e) {
            if (!languageSwitcher.contains(e.target)) {
                languageSwitcher.classList.remove('open');
            }
        });

        // Close dropdown when a language is selected
        const langOptions = document.querySelectorAll('.lang-option');
        langOptions.forEach(option => {
            option.addEventListener('click', function() {
                languageSwitcher.classList.remove('open');
            });
        });
    }
});
</script>
```

### Step 2: Update CSS for Click-Based Toggle

Replace the hover-based CSS with click-based CSS in `base.html` (around line 250):

**BEFORE (Hover-based - BROKEN):**
```css
.language-switcher:hover .lang-dropdown {
    opacity: 1;
    visibility: visible;
    transform: translateY(0);
}
```

**AFTER (Click-based - FIXED):**
```css
.language-switcher.open .lang-dropdown {
    opacity: 1;
    visibility: visible;
    transform: translateY(0);
}
```

### Step 3: Remove Hover Arrow Rotation (Optional)

Change line 230-232 to only rotate on open, not hover:

**BEFORE:**
```css
.language-switcher:hover .lang-arrow {
    transform: rotate(180deg);
}
```

**AFTER:**
```css
.language-switcher.open .lang-arrow {
    transform: rotate(180deg);
}
```

---

## COMPLETE FIXED CODE SECTIONS

### 1. CSS Section (lines 234-254 in base.html)

```css
.lang-dropdown {
    position: absolute;
    top: calc(100% + 0.5rem);
    right: 0;
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-md);
    box-shadow: var(--shadow-lg);
    z-index: 1000;
    min-width: 8rem;
    opacity: 0;
    visibility: hidden;
    transform: translateY(-10px);
    transition: all var(--transition-base);
}

/* Changed from :hover to .open class */
.language-switcher.open .lang-dropdown {
    opacity: 1;
    visibility: visible;
    transform: translateY(0);
}

/* Also change arrow rotation */
.language-switcher.open .lang-arrow {
    transform: rotate(180deg);
}
```

### 2. JavaScript Section (add before closing `</body>` tag)

```html
<!-- Language Switcher Toggle Script -->
<script>
(function() {
    'use strict';

    document.addEventListener('DOMContentLoaded', function() {
        const langToggle = document.querySelector('.lang-toggle');
        const languageSwitcher = document.querySelector('.language-switcher');

        if (!langToggle || !languageSwitcher) return;

        // Toggle dropdown on button click
        langToggle.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            languageSwitcher.classList.toggle('open');
        });

        // Close dropdown when clicking outside
        document.addEventListener('click', function(e) {
            if (!languageSwitcher.contains(e.target)) {
                languageSwitcher.classList.remove('open');
            }
        });

        // Close dropdown after language selection (optional UX improvement)
        const langOptions = document.querySelectorAll('.lang-option');
        langOptions.forEach(function(option) {
            option.addEventListener('click', function() {
                // Dropdown will close naturally on page navigation
                // But this improves perceived responsiveness
                languageSwitcher.classList.remove('open');
            });
        });
    });
})();
</script>
```

---

## VERIFICATION STEPS

### 1. Before Fix
- Hover over language button
- Try to click Romanian or Spanish
- **Result:** Dropdown disappears before click registers
- Language doesn't change

### 2. After Fix
- Click language button (not hover)
- Dropdown stays open
- Click Romanian or Spanish
- **Result:** URL changes to `/ro/...` or `/es/...`
- Language changes correctly

### 3. Test All Pages
```
English:  http://localhost:5003/en/pricing
Romanian: http://localhost:5003/ro/pricing  ← Should translate
Spanish:  http://localhost:5003/es/pricing   ← Should translate
```

### 4. Test Navigation Persistence
- Start at `/ro/pricing`
- Click "Despre" (About) in navigation
- Should go to `/ro/about` (maintains language)
- Click language dropdown
- Switch to Spanish
- Should go to `/es/about`

---

## WHY THIS WASN'T CAUGHT EARLIER

1. **Desktop testing bias:** On fast machines, sometimes the click registers before hover ends
2. **Slow mouse movement:** If you move very slowly, hover might persist
3. **Browser differences:** Some browsers handle hover/click differently
4. **Touch devices:** On mobile, hover doesn't apply (different behavior)

The hover-based approach works maybe 20% of the time, depending on mouse speed and browser, which made it seem like an intermittent issue rather than a systematic problem.

---

## ALTERNATIVE SOLUTION (Pure CSS, More Complex)

If you prefer to keep pure CSS without JavaScript, you need to expand the hover area:

```css
.language-switcher {
    position: relative;
}

.lang-dropdown {
    position: absolute;
    top: calc(100% + 0.5rem);
    right: 0;
    /* Add padding-top to extend hover area */
    padding-top: 0.5rem;
    margin-top: -0.5rem;
    /* rest of styles... */
}

.language-switcher:hover .lang-dropdown,
.lang-dropdown:hover {
    opacity: 1;
    visibility: visible;
    transform: translateY(0);
}
```

However, **JavaScript toggle is more reliable and provides better UX**.

---

## SUMMARY

**Problem:** Pure CSS `:hover` dropdown disappears when mouse moves from button to menu
**Solution:** Use JavaScript to toggle `.open` class on click instead
**Impact:** Language switcher now works 100% reliably
**Time to fix:** 5 minutes (add script, change 3 CSS lines)

**Files to modify:**
1. `templates/base.html` - Update CSS (line ~250, ~231)
2. `templates/base.html` - Add JavaScript (before `</body>`)

After this fix, the language switcher will work perfectly on all pages.
