# Southern Cities Enterprises - Global Header Component

## 🎯 Overview

A modern, responsive header/navbar component for the Southern Cities Enterprises website. Clean design with smooth animations, mobile-friendly navigation, and easy maintenance.

## 🎨 Design

### Visual Style
- **Background**: Navy (#132452)
- **Text**: White (#ffffff)
- **Accent**: Orange (#fa8c41) for hover/active states
- **Layout**: Logo left, Navigation right, CTA button
- **Position**: Sticky/fixed on scroll

### Features
- ✨ Clean, minimal layout
- 🎭 Smooth dropdown animations
- 📱 Responsive hamburger menu
- 🎯 Active page highlighting
- 🔘 "Get Started" CTA button
- ⚡ Professional hover effects

## 📁 File Structure

```
southern-cities-website/
├── header.html          # Global header component
├── load-header.js       # Header loader script
├── index.html          # Homepage (using new header)
├── services.html       # Services page (using new header)
├── blog.html           # Blog page (using new header)
├── general-contracting.html
├── acquisitions.html
├── brokerage.html
├── development.html
└── ... (all pages use the same header)
```

## 🚀 How It Works

### 1. Component File (header.html)
Contains the complete header with:
- HTML structure
- CSS styles (scoped to header)
- JavaScript functionality

### 2. Loader Script (load-header.js)
Simple fetch-based loader:
```javascript
fetch('header.html')
    .then(response => response.text())
    .then(html => {
        document.getElementById('header-placeholder').innerHTML = html;
    });
```

### 3. Page Integration
Every page includes:
```html
<!-- GLOBAL HEADER -->
<div id="header-placeholder"></div>
<script src="load-header.js"></script>
```

## 🔧 Customization

### Changing Colors
Edit `header.html` and update these values:
```css
.site-header {
    background-color: #132452; /* Navy */
}
.nav-link:hover,
.cta-button {
    color: #fa8c41; /* Orange */
}
```

### Modifying Navigation
Edit the menu structure in `header.html`:
```html
<ul class="nav-menu">
    <li class="nav-item">
        <a href="index.html" class="nav-link">Home</a>
    </li>
    <!-- Add more items here -->
</ul>
```

### Adding Dropdown Items
Add items to the Services dropdown:
```html
<div class="dropdown-menu">
    <a href="new-service.html">New Service</a>
</div>
```

## 📱 Responsive Behavior

### Desktop (> 968px)
- Full horizontal navigation
- Dropdown on hover
- 80px header height
- All items visible

### Tablet/Mobile (≤ 968px)
- Hamburger menu icon
- Slide-in mobile menu
- Stacked navigation
- Touch-friendly spacing

### Small Mobile (≤ 768px)
- Reduced logo size (40px)
- Adjusted padding
- Optimized for small screens

## 🎯 Navigation Structure

```
Home
About
Services ▾
    ├── General Contracting
    ├── Acquisitions
    ├── Brokerage
    ├── Development
    └── View All Services
Blog
Contact
[Get Started]  ← CTA Button
```

## ✨ Interactive Features

### Hover Effects
- Navigation links: Color change to orange
- Logo: Subtle scale (1.05x)
- CTA button: Background/border swap + shadow
- Dropdown items: Background + indent animation

### Dropdown Animation
```css
/* Smooth reveal */
opacity: 0 → 1
transform: translateY(-10px) → translateY(0)
transition: 0.3s ease
```

### Mobile Menu
- Hamburger icon animates to X
- Menu slides down smoothly
- Closes on outside click
- Closes on navigation
- Body scroll locked when open

### Active Page Highlighting
- Current page link highlighted in orange
- Underline indicator for active page
- Auto-detects page from URL
- Works for all pages including services

## 🛠️ Maintenance

### To Update the Header
1. Edit `header.html`
2. Save changes
3. Refresh any page to see updates
4. All pages automatically use new header

### To Add a New Page
1. Create your new HTML page
2. Add this code where header should appear:
```html
<div id="header-placeholder"></div>
<script src="load-header.js"></script>
```
3. Done! Header appears automatically

### To Modify Styles
- Desktop styles: Edit `.site-header` section
- Mobile styles: Edit `@media (max-width: 968px)` section
- Animations: Edit `transition` properties

## 📊 Performance

- **Header file size**: ~11KB (uncompressed)
- **Load time**: < 50ms (local)
- **JavaScript**: Vanilla (no frameworks)
- **CSS**: Scoped (no conflicts)
- **Compatibility**: All modern browsers

## ✅ Browser Support

- ✅ Chrome/Edge (Chromium) - Latest
- ✅ Firefox - Latest
- ✅ Safari - Latest
- ✅ Mobile Safari (iOS) - Latest
- ✅ Chrome Mobile (Android) - Latest

## 🐛 Troubleshooting

### Header Not Showing
- Check if `header.html` exists in same directory
- Check if `load-header.js` is loaded
- Check browser console for errors

### Dropdown Not Working
- Verify JavaScript is enabled
- Check for CSS conflicts
- Clear browser cache

### Mobile Menu Not Closing
- Ensure click event listener is working
- Check if menu-toggle has correct ID
- Verify JavaScript is not blocked

## 📚 Code Examples

### Active Page Detection
```javascript
const currentPage = window.location.pathname.split('/').pop() || 'index.html';
navLinks.forEach(link => {
    if (link.getAttribute('href') === currentPage) {
        link.classList.add('active');
    }
});
```

### Mobile Menu Toggle
```javascript
mobileToggle.addEventListener('click', function() {
    this.classList.toggle('active');
    headerNav.classList.toggle('active');
    document.body.style.overflow = headerNav.classList.contains('active') ? 'hidden' : '';
});
```

### Dropdown Animation
```css
.dropdown-menu {
    opacity: 0;
    visibility: hidden;
    transform: translateY(-10px);
    transition: all 0.3s ease;
}

.has-dropdown:hover .dropdown-menu {
    opacity: 1;
    visibility: visible;
    transform: translateY(0);
}
```

## 🎓 Best Practices

1. **Don't modify page-specific styles** - Keep all header styles in header.html
2. **Use semantic HTML** - Maintain accessibility
3. **Test on mobile devices** - Not just browser dev tools
4. **Keep JavaScript minimal** - Avoid heavy dependencies
5. **Cache busting** - Add version query string if needed (header.html?v=2)

## 📝 Change Log

### v1.0 (March 22, 2026)
- ✅ Initial header redesign
- ✅ Extracted to component
- ✅ Added dropdown animations
- ✅ Mobile menu implementation
- ✅ Active page highlighting
- ✅ Deployed to all pages

## 🤝 Contributing

To make changes:
1. Edit `header.html`
2. Test on all pages
3. Commit changes
4. Push to GitHub

## 📞 Support

For issues or questions:
- Check this documentation
- Review `HEADER-REDESIGN-SUMMARY.md`
- Review `DEPLOYMENT-CHECKLIST.md`

---

**Last Updated**: March 22, 2026  
**Version**: 1.0  
**Status**: Production Ready ✅
