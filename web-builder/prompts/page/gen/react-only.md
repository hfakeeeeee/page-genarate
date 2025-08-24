```jsx
import React, { useState } from 'react';
import { Link } from 'react-router-dom';

// FULL-PAGE LAYOUT TEMPLATE - Use this structure for all pages
export default function PageNamePage() {
  return (
    <div className="page-container">
      <style>
      {`
        .page-container {
          min-height: 100vh;
          width: 100%;
          background: var(--nt-color-background-base);
          font-family: var(--nt-font-family-default);
        }
        
        .page-header {
          width: 100%;
          padding: var(--nt-size-spacing-72) var(--nt-size-spacing-24);
          background: linear-gradient(135deg, var(--nt-color-humana-green), var(--nt-color-humana-teal));
          color: white;
          text-align: center;
        }
        
        .page-title {
          font-size: var(--nt-size-font-6xl);
          font-weight: var(--nt-font-weight-bold);
          margin: 0 0 var(--nt-size-spacing-16) 0;
        }
        
        .page-subtitle {
          font-size: var(--nt-size-font-xl);
          opacity: 0.9;
          margin: 0;
          max-width: 600px;
          margin: 0 auto;
        }
        
        .page-content {
          max-width: 1200px;
          margin: 0 auto;
          padding: var(--nt-size-spacing-72) var(--nt-size-spacing-24);
        }
        
        .content-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
          gap: var(--nt-size-spacing-32);
          margin-top: var(--nt-size-spacing-48);
        }
        
        .card {
          background: white;
          border-radius: var(--nt-size-radius-rounded);
          box-shadow: var(--nt-shadow-card);
          overflow: hidden;
          transition: transform 0.3s ease, box-shadow 0.3s ease;
          height: 100%;
        }
        
        .card:hover {
          transform: translateY(-8px);
          box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        }
        
        .card-image {
          width: 100%;
          height: 250px;
          object-fit: cover;
          background: var(--nt-color-background-gray-100);
          transition: transform 0.3s ease;
        }
        
        .card:hover .card-image {
          transform: scale(1.05);
        }
        
        .card-content {
          padding: var(--nt-size-spacing-24);
          display: flex;
          flex-direction: column;
          gap: var(--nt-size-spacing-12);
        }
        
        .card-title {
          font-size: var(--nt-size-font-xl);
          font-weight: var(--nt-font-weight-semibold);
          color: var(--nt-color-font-heading);
          margin: 0;
        }
        
        .card-description {
          color: var(--nt-color-font-secondary);
          line-height: var(--nt-font-line-height-comfortable);
          margin: 0;
          flex-grow: 1;
        }
        
        .btn-primary {
          background: var(--nt-color-action-primary-default);
          color: white;
          border: none;
          padding: var(--nt-size-spacing-16) var(--nt-size-spacing-24);
          border-radius: var(--nt-size-radius-fine);
          font-weight: var(--nt-font-weight-medium);
          cursor: pointer;
          text-decoration: none;
          display: inline-flex;
          align-items: center;
          justify-content: center;
          gap: var(--nt-size-spacing-8);
          transition: all 0.2s ease;
          margin-top: auto;
        }
        
        .btn-primary:hover {
          background: var(--nt-color-action-primary-active);
          transform: translateY(-2px);
        }
        
        .search-section {
          background: var(--nt-color-background-gray-050);
          padding: var(--nt-size-spacing-72) var(--nt-size-spacing-24);
          text-align: center;
        }
        
        .search-container {
          max-width: 600px;
          margin: 0 auto;
          display: flex;
          gap: var(--nt-size-spacing-12);
        }
        
        .search-input {
          flex: 1;
          padding: var(--nt-size-spacing-16);
          border: 2px solid var(--nt-color-grayscale-200);
          border-radius: var(--nt-size-radius-fine);
          font-size: var(--nt-size-font-base);
          transition: border-color 0.2s ease;
        }
        
        .search-input:focus {
          outline: none;
          border-color: var(--nt-color-action-primary-default);
        }
        
        .hero-section {
          display: flex;
          align-items: center;
          gap: var(--nt-size-spacing-48);
          margin-bottom: var(--nt-size-spacing-72);
        }
        
        .hero-content {
          flex: 1;
        }
        
        .hero-image {
          flex: 1;
          max-width: 500px;
          height: auto;
          border-radius: var(--nt-size-radius-rounded);
          box-shadow: var(--nt-shadow-card);
        }
        
        .icon-svg {
          width: 24px;
          height: 24px;
          fill: currentColor;
        }
        
        .rating {
          display: flex;
          align-items: center;
          gap: var(--nt-size-spacing-4);
          color: var(--nt-color-humana-gold);
        }
        
        @media (max-width: 768px) {
          .page-title {
            font-size: var(--nt-size-font-4xl);
          }
          
          .content-grid {
            grid-template-columns: 1fr;
            gap: var(--nt-size-spacing-24);
          }
          
          .page-content, .search-section {
            padding: var(--nt-size-spacing-48) var(--nt-size-spacing-16);
          }
          
          .hero-section {
            flex-direction: column;
            text-align: center;
          }
          
          .search-container {
            flex-direction: column;
          }
        }
      `}
      </style>
      
      {/* HEADER SECTION */}
      <header className="page-header">
        <h1 className="page-title">Page Title</h1>
        <p className="page-subtitle">Page subtitle or description</p>
      </header>
      
      {/* MAIN CONTENT */}
      <main className="page-content">
        {/* Content goes here */}
      </main>
    </div>
  );
}
```

## CRITICAL REQUIREMENTS:
1. **FULL PAGE LAYOUT**: Always use min-height: 100vh for full page coverage
2. **IMAGES**: Use https://source.unsplash.com/random/[width]x[height]?[keyword] for ALL book covers and photos
3. **ICONS**: Use inline SVG elements for icons (search, star, etc.) - NOT images
4. **RESPONSIVE**: Mobile-first design with proper breakpoints
5. **MODERN**: Clean typography, proper spacing, subtle shadows and hover effects
6. **PERFORMANCE**: Always include React import, use semantic HTML
