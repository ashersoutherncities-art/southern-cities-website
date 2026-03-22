# E-Commerce Integration Guide
## Southern Cities Website - Backend Setup

This guide covers how to integrate real payment processing, form handling, and deploy the site.

---

## 🔐 Stripe Integration (Payment Processing)

### Step 1: Get Stripe API Keys

1. Sign up at [stripe.com](https://stripe.com)
2. Navigate to **Developers → API Keys**
3. Copy your **Publishable Key** and **Secret Key**
   - Use **Test Mode** keys initially (start with `pk_test_` and `sk_test_`)
   - Switch to **Live Mode** when ready for production

### Step 2: Update Frontend (checkout.html)

Replace the placeholder on **line 389**:

```javascript
// REPLACE THIS:
const stripe = Stripe('pk_test_51234567890abcdefghijklmnopqrstuvwxyz');

// WITH YOUR ACTUAL TEST KEY:
const stripe = Stripe('pk_test_YOUR_ACTUAL_PUBLISHABLE_KEY_HERE');
```

### Step 3: Create Backend API Endpoint

You need a server endpoint to create Payment Intents. Here's a **Node.js/Express** example:

```javascript
// server.js
const express = require('express');
const stripe = require('stripe')('sk_test_YOUR_SECRET_KEY_HERE');
const app = express();

app.use(express.json());
app.use(express.static('public')); // Serve your HTML files

// Create Payment Intent
app.post('/api/create-payment-intent', async (req, res) => {
  try {
    const { cart, billingDetails } = req.body;
    
    // Calculate total
    const amount = cart.reduce((sum, item) => sum + item.price, 0) * 100; // Stripe uses cents
    
    // Separate one-time and subscriptions
    const oneTimeItems = cart.filter(item => !item.isSubscription);
    const subscriptionItems = cart.filter(item => item.isSubscription);
    
    if (oneTimeItems.length > 0) {
      // Create Payment Intent for one-time items
      const paymentIntent = await stripe.paymentIntents.create({
        amount: oneTimeItems.reduce((sum, item) => sum + item.price, 0) * 100,
        currency: 'usd',
        metadata: {
          customer_name: billingDetails.name,
          customer_email: billingDetails.email,
          items: JSON.stringify(oneTimeItems.map(i => i.name))
        }
      });
      
      res.json({ clientSecret: paymentIntent.client_secret });
    }
    
    // Handle subscriptions separately (see below)
    
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.listen(3000, () => console.log('Server running on port 3000'));
```

### Step 4: Handle Subscriptions

For recurring services, use Stripe Subscriptions:

```javascript
// Create Subscription
app.post('/api/create-subscription', async (req, res) => {
  try {
    const { cart, billingDetails, paymentMethodId } = req.body;
    
    // Create customer
    const customer = await stripe.customers.create({
      email: billingDetails.email,
      name: billingDetails.name,
      payment_method: paymentMethodId,
      invoice_settings: {
        default_payment_method: paymentMethodId,
      },
    });
    
    // Create subscription for each recurring item
    const subscriptions = [];
    for (const item of cart.filter(i => i.isSubscription)) {
      // First, create a product and price in Stripe dashboard or via API
      const subscription = await stripe.subscriptions.create({
        customer: customer.id,
        items: [{ price: item.stripePriceId }], // You'll create these in Stripe
        expand: ['latest_invoice.payment_intent'],
      });
      subscriptions.push(subscription);
    }
    
    res.json({ subscriptions });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});
```

### Step 5: Create Products in Stripe Dashboard

1. Go to **Products** in Stripe Dashboard
2. Create products for each service:
   - **Cost Estimate - Basic** → $150 (one-time)
   - **Deal Sourcing - Access** → $297/month (recurring)
   - etc.
3. Copy the **Price ID** (starts with `price_`) for each
4. Store these in your frontend or database

### Step 6: Uncomment Real Implementation Code

In `checkout.html`, uncomment the "REAL IMPLEMENTATION" section (lines 460-490) and remove the demo timeout.

---

## 📧 Form Integration (Contact & Newsletter)

### Option A: Netlify Forms (Easiest)

1. Deploy to Netlify
2. Add `netlify` attribute to your forms:

```html
<form name="contact" method="POST" data-netlify="true">
  <input type="hidden" name="form-name" value="contact">
  <!-- rest of form fields -->
</form>
```

3. Submissions appear in **Netlify Dashboard → Forms**

### Option B: FormSpree

1. Sign up at [formspree.io](https://formspree.io)
2. Update form action:

```html
<form action="https://formspree.io/f/YOUR_FORM_ID" method="POST">
  <!-- form fields -->
</form>
```

### Option C: Custom Backend

```javascript
// Add to server.js
app.post('/api/contact', async (req, res) => {
  const { name, email, phone, service, message } = req.body;
  
  // Send email using SendGrid, AWS SES, or similar
  const sgMail = require('@sendgrid/mail');
  sgMail.setApiKey(process.env.SENDGRID_API_KEY);
  
  await sgMail.send({
    to: 'info@southerncitiesinvestors.com',
    from: 'website@southerncitiesinvestors.com',
    subject: `New Contact Form: ${service}`,
    text: `From: ${name} (${email})\nPhone: ${phone}\n\n${message}`,
    html: `<p><strong>From:</strong> ${name} (${email})<br><strong>Phone:</strong> ${phone}</p><p>${message}</p>`
  });
  
  res.json({ success: true });
});

// Newsletter signup
app.post('/api/newsletter-subscribe', async (req, res) => {
  const { email } = req.body;
  
  // Add to Mailchimp, ConvertKit, or your email service
  // Example with Mailchimp:
  const mailchimp = require('@mailchimp/mailchimp_marketing');
  mailchimp.setConfig({
    apiKey: process.env.MAILCHIMP_API_KEY,
    server: 'us10', // Your datacenter
  });
  
  await mailchimp.lists.addListMember('YOUR_LIST_ID', {
    email_address: email,
    status: 'subscribed',
  });
  
  res.json({ success: true });
});
```

---

## 🚀 Deployment

### Option 1: Netlify (Recommended for Static + Forms)

```bash
# Install Netlify CLI
npm install -g netlify-cli

# Deploy
cd southern-cities-website
netlify deploy --prod

# Or connect GitHub repo for auto-deploys
netlify init
```

**Advantages:**
- Free SSL
- Automatic HTTPS
- Built-in form handling
- CI/CD from GitHub
- CDN included

### Option 2: Vercel (Good for Next.js/React)

```bash
npm install -g vercel
vercel
```

### Option 3: Traditional Hosting (cPanel/HostGator/BlueHost)

1. **Backup current site** (if exists)
2. Upload files via FTP/cPanel File Manager to `public_html/`
3. Ensure `.htaccess` for clean URLs:

```apache
RewriteEngine On
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule ^([^\.]+)$ $1.html [NC,L]
```

4. Update nameservers if needed

### Option 4: GitHub Pages (Free Static Hosting)

```bash
# In your repo
git add .
git commit -m "E-commerce upgrade"
git push origin main

# Enable GitHub Pages in repo settings
# Choose main branch, / (root)
```

**Note:** GitHub Pages doesn't support server-side code, so use external services for forms/payments.

---

## 🔧 Backend File Structure (If Using Node.js)

```
southern-cities-website/
├── public/                  # Frontend files
│   ├── index.html          # Use index-enhanced.html
│   ├── services.html
│   ├── blog.html
│   ├── checkout.html
│   ├── order-confirmation.html
│   └── assets/
├── server.js               # Express backend
├── package.json
├── .env                    # Store API keys (DON'T COMMIT THIS)
└── README.md
```

**Install dependencies:**

```bash
npm init -y
npm install express stripe cors dotenv @sendgrid/mail
```

**Create .env file:**

```
STRIPE_SECRET_KEY=sk_test_YOUR_KEY
STRIPE_PUBLISHABLE_KEY=pk_test_YOUR_KEY
SENDGRID_API_KEY=your_sendgrid_key
```

**Update server.js:**

```javascript
require('dotenv').config();
const express = require('express');
const cors = require('cors');
const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY);

const app = express();
app.use(cors());
app.use(express.json());
app.use(express.static('public'));

// Add endpoints from examples above

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Server on port ${PORT}`));
```

---

## 📊 Analytics & Tracking

### Google Analytics 4

Add to `<head>` of all pages:

```html
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
```

### Facebook Pixel (Optional)

```html
<script>
  !function(f,b,e,v,n,t,s)
  {if(f.fbq)return;n=f.fbq=function(){n.callMethod?
  n.callMethod.apply(n,arguments):n.queue.push(arguments)};
  if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
  n.queue=[];t=b.createElement(e);t.async=!0;
  t.src=v;s=b.getElementsByTagName(e)[0];
  s.parentNode.insertBefore(t,s)}(window, document,'script',
  'https://connect.facebook.net/en_US/fbevents.js');
  fbq('init', 'YOUR_PIXEL_ID');
  fbq('track', 'PageView');
</script>
```

---

## ✅ Launch Checklist

### Before Going Live:

- [ ] Replace Stripe test keys with live keys
- [ ] Test all payment flows (one-time + subscriptions)
- [ ] Test contact form submission
- [ ] Test newsletter signup
- [ ] Verify all links work
- [ ] Check mobile responsiveness
- [ ] Test on Chrome, Safari, Firefox, Edge
- [ ] Add SSL certificate (auto with Netlify/Vercel)
- [ ] Set up Google Analytics
- [ ] Create backup of current site
- [ ] Test shopping cart functionality
- [ ] Verify pricing matches scalable-services-report.md
- [ ] Add legal pages (Privacy Policy, Terms of Service)
- [ ] Set up order confirmation emails
- [ ] Test order management workflow

### After Launch:

- [ ] Monitor Stripe dashboard for payments
- [ ] Check form submissions daily
- [ ] Set up email notifications for new orders
- [ ] Create internal order fulfillment process
- [ ] Document how to add new services
- [ ] Train team on order management
- [ ] Set up customer support email/phone routing

---

## 🛡️ Security Best Practices

1. **Never expose secret keys** in frontend code
2. Use **environment variables** for sensitive data
3. Validate all form inputs on backend
4. Use **HTTPS** (automatic with Netlify/Vercel)
5. Implement rate limiting on API endpoints
6. Store customer data securely (GDPR/CCPA compliant)
7. Regular dependency updates (`npm audit fix`)

---

## 📞 Support Resources

- **Stripe Docs:** [stripe.com/docs](https://stripe.com/docs)
- **Netlify Docs:** [docs.netlify.com](https://docs.netlify.com)
- **FormSpree:** [formspree.io/guides](https://formspree.io/guides)
- **GitHub Deployment:** [pages.github.com](https://pages.github.com)

---

## 🔄 Next Steps

1. **Replace index.html** with index-enhanced.html:
   ```bash
   mv index.html index-old.html
   mv index-enhanced.html index.html
   ```

2. **Update Stripe keys** in checkout.html

3. **Choose deployment method** and deploy

4. **Set up form handling** (Netlify/FormSpree/custom)

5. **Test thoroughly** in test mode

6. **Go live** and update DNS if needed

---

**Questions?** Contact the development team or refer to the documentation links above.
