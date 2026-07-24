# Site Audit - https://www.boatwindowsltd.co.uk/

**Date:** 2026-04-14
**Mode:** Production
**Pentest:** Disabled
**Pages audited:** 5

---

## Summary

| Category | Score | Rating | Key Finding |
|---|---|---|---|
| Accessibility | 94/100 | Pass | Colour contrast failures across all pages; heading hierarchy skips levels |
| UX | 6/10 | Needs Work | Functional but generic - vague CTAs, no wayfinding, slow perceived speed |
| Design | 6/10 | Needs Work | Competent Squarespace template elevated by good photography, but generic palette and layout |
| Security | 5/10 | Needs Work | Missing CSP, Referrer-Policy, and Permissions-Policy headers; cookies lack HttpOnly and SameSite |
| SEO | 98/100 | Pass | Strong fundamentals; incomplete structured data and one non-descriptive link |

**Overall:** Boat Windows LTD presents a professional, trustworthy face for a niche manufacturer. The photography is excellent and the messaging is clear. However, significant performance problems (7-13s LCP across pages), widespread colour contrast failures, missing security headers, and a generic visual identity hold it back. The site works but doesn't impress - fixing the performance and contrast issues would have the biggest immediate impact on user experience and accessibility compliance.

---

## Accessibility

### Score: 94/100 (Lighthouse average across 5 pages)

### WCAG Violations

**Colour contrast (WCAG 2.1 AA - 1.4.3)** - found on every page:

| Page | Errors | Key Affected Elements |
|---|---|---|
| Homepage | 10 | Cookie banner buttons, h1 heading text, CTA buttons, footer text |
| About | 29 | Cookie banner, h1, h2 headings, body text, form field labels, CTA buttons |
| Windows | 10 | Cookie banner, h1, CTA buttons, footer text/links |
| Testimonials | 16 | Cookie banner, h1, testimonial text, CTA buttons, footer |
| Contact | 8 | Cookie banner, form submit button, body text, footer text |

Common failing selectors:
- `section.gdpr-cookie-banner > div.button-group > button > span` - cookie banner buttons fail contrast on every page
- `span.sqsrte-text-color--lightAccent` - light accent headings over images lack sufficient contrast
- `div.sqs-html-content > p` - footer/contact section body text is too low contrast
- Form field labels on About/Contact pages fail 4.5:1 ratio

**Heading hierarchy (WCAG 2.1 A - 1.3.1)** - found on every page:

| Page | Issue |
|---|---|
| Homepage | h1 > h2 > h4 (skips h3) in footer section |
| About | No h1; h2 > h3 > h4 (footer skips to h4) |
| Windows | No h1; h2 > h4 (skips h3) |
| Testimonials | No h1; h2 > h3 > h4 (footer skips) |
| Contact | h1 > h4 (skips h2 and h3 in footer) |

### Manual Findings

**Keyboard navigation:**
- Skip link (`#page`) present in source but destination element may not exist
- Mobile menu toggle buttons lack `aria-expanded` state
- Menu open/close buttons lack descriptive `aria-label` attributes
- Navigation appears duplicated (desktop + mobile) without proper `aria-hidden` toggling

**Screen reader semantics:**
- No `<main>` landmark region detected
- No `<nav>` semantic wrapper around navigation
- No `<footer>` semantic element
- Images generally have good descriptive alt text
- Logo images on Windows page lack alt text in some instances

**Focus indicators:**
- Relies on Squarespace defaults; no custom focus styling observed

**Motion:**
- No `prefers-reduced-motion` media query detected in custom styles

---

## UX Review

### Score: 6/10

**Navigation:**
- Clear 5-item top navigation: Home, About, Windows, Testimonials, Contact
- Mobile hamburger menu present
- No breadcrumbs on any page
- No visible active state indicating current page in navigation
- No `aria-current="page"` attribute on active nav items
- Site structure is flat (single level) so navigation is simple enough to follow

**Interactions:**
- CTA buttons use generic text ("Learn more", "Contact Us") without specifying what the user will get
- Cookie banner present with Accept/Manage options
- Contact form exists but form validation approach is unclear from source
- No visible loading states or skeleton loaders
- Button hover/focus states rely on Squarespace defaults

**Mobile experience:**
- Hamburger menu indicates mobile responsive design
- Squarespace CDN serves responsive images via `srcset`
- Viewport meta tag correctly set (`width=device-width, initial-scale=1`)
- Tap targets on cookie banner buttons may be undersized based on contrast selector analysis

**Performance perception:**
- Site feels slow - FCP averages 3.8s across pages
- LCP is critically poor: 6.8s (best, testimonials) to 12.6s (worst, windows)
- Total Blocking Time is high: 430ms (testimonials) to 1,110ms (homepage)
- Time to Interactive ranges from 11.1s to 20.2s
- Windows page has significant CLS (0.386) causing layout shift
- Heavy reliance on Squarespace's JavaScript bundle causes long blocking time
- No visible skeleton loaders or progressive loading during the long initial load

---

## Design Critique

### Score: 6/10

**Visual hierarchy:**
- Homepage has a clear top-down flow: hero > introduction > value props > contact
- The "Simple, Stylish, Slimline, Safe, Secure" section uses alliteration effectively as a mnemonic
- Heading sizes create reasonable hierarchy but light accent colours on image backgrounds reduce readability
- Footer contact section competes for attention equally with body content

**Typography:**
- Uses Squarespace's default system/template fonts - clean but undistinctive
- Sans-serif choices are appropriate for a manufacturing business but don't express craft or precision
- Type scale appears consistent within sections
- Body text is readable at standard sizes
- No distinctive display font to give the brand character

**Colour:**
- Palette is neutral/minimal: predominantly white, dark text, with photography providing colour
- No distinctive brand colour beyond the logo
- The restrained approach is clean but forgettable
- Light accent text colour used on hero sections fails contrast and looks washed out
- Footer section uses a darker background but contrast ratios still fail

**Spacing & layout:**
- Generous whitespace throughout - content has room to breathe
- Sections are clearly separated
- Layout is conventional and predictable (full-width sections stacked vertically)
- Squarespace grid system provides consistent alignment
- No surprising or memorable compositional choices

**Consistency:**
- Button styles are consistent across pages
- Image treatment (full-width, high quality) is uniform
- Footer appears identical on all pages
- The site feels cohesive, though that's partly because of the template constraints

**Overall impression:**
- This is a well-executed Squarespace template with good content and excellent photography
- The photography is by far the strongest design element - real boat images build trust
- The weakest element is the colour palette - there's nothing that says "marine" or "craft"
- The site doesn't look like a template per se, but it doesn't have distinctive character either
- You'd remember the product, not the website

---

## Security

### Score: 5/10

### HTTP Headers

| Header | Status | Value |
|---|---|---|
| Strict-Transport-Security | Present | `max-age=15552000` (~180 days) |
| Content-Security-Policy | **Missing** | Not set |
| X-Content-Type-Options | Present | `nosniff` |
| X-Frame-Options | Present | `SAMEORIGIN` |
| Referrer-Policy | **Missing** | Not set |
| Permissions-Policy | **Missing** | Not set |

**Notes:**
- HSTS max-age of 15552000 is adequate but could be longer (31536000 recommended)
- No `includeSubDomains` or `preload` directives on HSTS
- Server header exposes `Squarespace` - minor information disclosure

### Cookie Flags

| Cookie | Secure | HttpOnly | SameSite |
|---|---|---|---|
| `crumb` (CSRF token) | Yes | **No** | **Not set** |

The `crumb` cookie is Squarespace's CSRF protection token. It has the `Secure` flag but lacks `HttpOnly` (accessible via JavaScript) and `SameSite` (no cross-site protection).

### Exposed Files

| Path | Response |
|---|---|
| `/.env` | 403 Forbidden |
| `/.git/config` | 403 Forbidden |
| `/package.json` | 404 Not Found |
| `/.DS_Store` | 403 Forbidden |

No sensitive files exposed. Squarespace's infrastructure blocks common sensitive paths.

### Form Security

- Contact form action uses HTTPS (Squarespace handles this)
- CSRF protection via `crumb` cookie is present
- Form fields are standard contact fields (name, email, message) - no sensitive data leakage
- No hidden fields exposing internal IDs or configuration observed

---

## SEO

### Score: 98/100 (Lighthouse average: homepage 92, all others 100)

**Meta tags:**

| Page | Title | Description | OG Tags | Twitter Card | Canonical |
|---|---|---|---|---|---|
| Homepage | "Boat Windows LTD \| Bespoke Narrowboat & Widebeam Boat Windows" (62 chars) | Present, 186 chars (slightly over 160 ideal) | Present (title, description, image, type) | Present (title) | Present |
| About | Present | Present | Present | Present | Present |
| Windows | Present | Present | Present | Present | Present |
| Testimonials | Present | Present | Present | Present | Present |
| Contact | Present | Present | Present | Present | Present |

**Issues found:**
- Homepage meta description at ~186 characters exceeds the 150-160 character ideal - may be truncated in SERPs
- `og:image` uses HTTP protocol (`http://static1.squarespace.com/...`) instead of HTTPS
- Twitter card meta tags present but missing `twitter:card` type declaration

**Heading structure:**
- Homepage: h1 present ("Boat Windows Ltd")
- About: **No h1** - first heading is h2
- Windows: **No h1** - first heading is h2
- Testimonials: **No h1** - first heading is h2
- Contact: h1 present ("Contact Us")

**URL structure:**
- Clean, readable slugs: `/about`, `/windows`, `/testimonials`, `/contact`
- No query string clutter

**Internal linking:**
- Pages cross-link via navigation and CTA buttons
- Homepage links to `/about` ("Learn more") and contact section
- Each product/content page links to `/contact` via CTA
- No orphan pages detected

**Link text:**
- Homepage has a non-descriptive "Learn more" link (flagged by Lighthouse)
- Fix: Change to "Learn more about our windows" or similar

**Structured data:**
- `WebSite` schema present but `description` field is empty
- `LocalBusiness` schema present but `address` and `openingHours` fields are empty
- No `Product` or `Service` schema for window products
- Squarespace generates these automatically but they need manual population

**Crawlability:**
- `robots.txt` present with standard Squarespace directives
- `sitemap.xml` present and valid with image extensions
- All pages indexable (no accidental `noindex`)
- Sitemap includes all 5 pages with image references

**Core Web Vitals (from Lighthouse):**

| Metric | Homepage | About | Windows | Testimonials | Contact |
|---|---|---|---|---|---|
| LCP | 7.1s | 10.8s | 12.6s | 6.8s | 10.5s |
| CLS | 0.003 | 0.094 | 0.386 | 0.11 | 0.09 |
| TBT* | 1,110ms | 860ms | 700ms | 430ms | 610ms |

*TBT is used as a proxy for INP in lab data. All LCP values far exceed the 2.5s "good" threshold.

---

## Recommendations

### Critical (fix immediately)

- [ ] **Fix colour contrast across all pages** - The `lightAccent` text colour on image backgrounds and footer body text both fail WCAG AA. Increase text contrast to at least 4.5:1 for normal text and 3:1 for large text. Affects: cookie banner buttons, hero headings, footer contact text, form labels. In Squarespace, adjust the colour theme's "Light Accent" value to a darker shade, and ensure footer text uses a colour with sufficient contrast against the background.

- [ ] **Fix heading hierarchy on all pages** - About, Windows, and Testimonials pages are missing h1 elements. Footer section jumps from h1/h2 to h4 on every page, skipping h3. Change footer "Location" and "Contact" headings from h4 to h3 (or style them as paragraphs with bold text if they don't warrant heading semantics). Add h1 headings to pages that lack them.

- [ ] **Improve Largest Contentful Paint** - LCP ranges from 6.8s to 12.6s across pages (target: under 2.5s). This is a Squarespace platform limitation but can be partially mitigated: ensure hero images are optimally sized (not oversized source files), enable Squarespace's built-in lazy loading, reduce the number of image blocks loading above the fold, and consider whether fewer/smaller hero images could work.

### Important (fix soon)

- [ ] **Add missing security headers** - Configure Content-Security-Policy, Referrer-Policy, and Permissions-Policy headers. On Squarespace, this requires using the Code Injection feature or a third-party CDN/proxy (like Cloudflare) to add headers, as Squarespace doesn't expose header configuration natively.

- [ ] **Add HttpOnly and SameSite flags to cookies** - The `crumb` CSRF cookie lacks `HttpOnly` and `SameSite` attributes. This is a Squarespace platform default and may not be directly configurable. Consider raising with Squarespace support or adding a proxy layer.

- [ ] **Fix CLS on Windows page** - CLS of 0.386 far exceeds the 0.1 "good" threshold. Likely caused by images loading without reserved dimensions. Ensure all images in the Windows page have explicit width/height or use Squarespace's aspect ratio settings to reserve space.

- [ ] **Complete structured data** - The `LocalBusiness` schema has empty `address` and `openingHours` fields. Populate with: "Unit 5a, Hopton Court, Hopton Road, Devizes SN10 2EU" and business hours. The `WebSite` schema has an empty `description` - add the meta description text.

- [ ] **Add `aria-label` and `aria-expanded` to mobile menu toggle** - The hamburger menu open/close buttons lack screen reader context. Add `aria-label="Open navigation menu"` and toggle `aria-expanded` between true/false via Squarespace's Code Injection or custom JavaScript.

- [ ] **Fix og:image protocol** - The Open Graph image URL uses `http://` instead of `https://`. Update to HTTPS to avoid mixed content warnings when social platforms fetch the preview image.

- [ ] **Change "Learn more" to descriptive link text** - The homepage CTA "Learn more" is vague. Change to "Learn more about our boat windows" or "About our clamp-in windows" to improve both SEO and accessibility.

### Nice to Have (polish)

- [ ] **Add semantic landmarks** - Wrap navigation in `<nav>`, main content in `<main>`, and footer in `<footer>`. This improves screen reader navigation. Achievable via Squarespace Code Injection adding ARIA roles to existing containers.

- [ ] **Add active state to current nav item** - Use `aria-current="page"` and visible styling on the active navigation link so users know which page they're on.

- [ ] **Strengthen the colour palette** - The site lacks a distinctive brand colour beyond the logo. Consider introducing a marine-inspired accent (deep navy, teal, or ocean blue) to buttons, headings, and interactive elements. This would make the brand more memorable.

- [ ] **Improve CTA copy** - "Learn more" and generic "Contact Us" buttons could be more specific: "See our window range", "Get a free quote", "Request a callback". Stronger CTAs would improve conversion.

- [ ] **Add `prefers-reduced-motion` support** - Add a media query to reduce or disable animations for users who prefer reduced motion. Can be added via Squarespace's Custom CSS injection.

- [ ] **Shorten homepage meta description** - Currently ~186 characters; trim to 150-160 to prevent SERP truncation.

- [ ] **Add Product/Service structured data** - Beyond the basic `LocalBusiness` schema, add `Product` or `Service` schema for the S Type and SX Type window ranges. This could enable rich results in search.

- [ ] **Extend HSTS max-age** - Current value is 15552000 (180 days). Increase to 31536000 (1 year) and add `includeSubDomains; preload` for HSTS preload list eligibility.
