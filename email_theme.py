"""
MessyMind Email Theme Configuration
====================================

Email-safe design tokens extracted from MessyMind Jekyll site.
Aligned with actual CSS from _sass/ directory.

Source files:
- _sass/_messymind-variables.scss (color palette)
- _sass/components/_newsletter-form.scss (component styles)
- _sass/bootstrap-purged.scss (layout)

This file is meant to be imported in Django BlogManager's email system.
All colors use hex format (email-safe, no rgba).
All fonts use web-safe stacks (no custom font loading).

Usage:
    from email_theme import EmailTheme
    
    # In templates
    <a style="background: {{ email_theme.colors.cta_bg }}; ...">Click</a>
"""

class EmailTheme:
    """
    MessyMind email design system.
    Email client safe (Gmail, Outlook, Apple Mail, etc.)
    """
    
    # =========================================================================
    # COLORS
    # =========================================================================
    class Colors:
        """Email-safe color palette"""
        
        # Backgrounds & containers
        background = "#ffffff"  # Main email background
        container = "#ffffff"   # Content container (usually same as background)
        
        # Text colors
        text = "#2E3D49"        # Primary text (dark slate)
        muted = "#6B7280"       # Secondary/helper text (medium gray)
        
        # Brand color
        primary = "#4F8A8B"     # Primary teal (headings, links)
        
        # Call-to-action
        cta_bg = "#F97F51"      # CTA button background (accent orange - SOLID, no gradient)
        cta_text = "#ffffff"    # CTA button text (white)
        
        # Borders & dividers
        border = "#D1D5DB"      # Input borders, HR, dividers (light gray)
        
        # Feedback states (email-safe: solid colors only)
        success_bg = "#E8F4F2"   # Success message background (light teal)
        success_text = "#2E5656" # Success text (dark teal)
        error_bg = "#FCE8E6"     # Error message background (light red)
        error_text = "#8B2323"   # Error text (dark red)
    
    colors = Colors
    
    # =========================================================================
    # TYPOGRAPHY
    # =========================================================================
    class Typography:
        """Email-safe font stacks (no custom fonts - load issues in email)"""
        
        # Body text - use Arial by default for maximum compatibility
        font_primary = "Arial, Helvetica, sans-serif"
        
        # Alternative serif stack (for accent text if needed)
        # NOTE: Georgia renders reliably in most email clients
        font_secondary = "Georgia, serif"
        
        # System fallback (if available in email client)
        font_system = "-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"
        
        # Font sizes (in px - email clients don't reliably support rem/em)
        size_base = "16px"
        size_sm = "14px"
        size_lg = "18px"
        
        # Font weights
        weight_normal = "400"
        weight_bold = "700"
        
        # Line heights
        line_height_text = "1.6"
        line_height_heading = "1.3"
    
    typography = Typography
    
    # =========================================================================
    # COMPONENTS
    # =========================================================================
    class Components:
        """Component-specific styling"""
        
        # Buttons
        button_radius = "6px"
        button_padding = "12px 24px"
        button_font_size = "16px"
        button_font_weight = "600"
        
        # Input-like styling (if needed for display purposes)
        input_radius = "6px"
        input_border_width = "2px"
        input_border_color = "#D1D5DB"
        
        # Cards/sections
        card_radius = "6px"
        card_padding = "20px"
        card_border = f"1px solid #D1D5DB"
    
    components = Components
    
    # =========================================================================
    # SPACING
    # =========================================================================
    class Spacing:
        """Email spacing utilities"""
        
        # Standard gaps
        gap_xs = "4px"
        gap_sm = "8px"
        gap_md = "12px"
        gap_lg = "16px"
        gap_xl = "24px"
        
        # Padding
        padding_sm = "8px"
        padding_md = "12px"
        padding_lg = "16px"
        
        # Email-safe container max width
        container_max_width = "600px"
        container_padding = "20px"
    
    spacing = Spacing
    
    # =========================================================================
    # BREAKPOINTS & RESPONSIVE
    # =========================================================================
    class Responsive:
        """Email responsive breakpoints"""
        
        # Mobile-first approach
        mobile_breakpoint = "480px"
        tablet_breakpoint = "640px"
        
        # For media queries in email
        # NOTE: Limited email client support for media queries
        # Prefer hybrid/fluid approach
    
    responsive = Responsive
    
    # =========================================================================
    # UTILITIES
    # =========================================================================
    
    @classmethod
    def get_button_style(cls, full=False):
        """
        Generate inline CSS for CTA button.
        
        Args:
            full (bool): Include all properties or just essentials
        
        Returns:
            str: Inline CSS style attribute value
        
        Example:
            <a href="..." style="{{ email_theme.get_button_style() }}">
        """
        essentials = (
            f"background-color: {cls.colors.cta_bg}; "
            f"color: {cls.colors.cta_text}; "
            f"border-radius: {cls.components.button_radius}; "
            f"padding: {cls.components.button_padding}; "
            f"font-weight: {cls.typography.weight_bold}; "
            f"text-decoration: none; "
            f"display: inline-block; "
        )
        
        if full:
            return (
                essentials +
                f"border: none; "
                f"cursor: pointer; "
                f"font-family: {cls.typography.font_primary}; "
                f"font-size: {cls.components.button_font_size}; "
                f"line-height: {cls.typography.line_height_text}; "
                f"text-align: center;"
            )
        return essentials
    
    @classmethod
    def get_text_style(cls, size='base', weight='normal', color='text'):
        """
        Generate inline CSS for text elements.
        
        Args:
            size (str): 'base', 'sm', or 'lg'
            weight (str): 'normal' or 'bold'
            color (str): Color key from Colors class
        
        Returns:
            str: Inline CSS style attribute value
        """
        size_map = {
            'base': cls.typography.size_base,
            'sm': cls.typography.size_sm,
            'lg': cls.typography.size_lg,
        }
        
        weight_map = {
            'normal': cls.typography.weight_normal,
            'bold': cls.typography.weight_bold,
        }
        
        color_value = getattr(cls.colors, color, cls.colors.text)
        
        return (
            f"font-family: {cls.typography.font_primary}; "
            f"font-size: {size_map.get(size, cls.typography.size_base)}; "
            f"font-weight: {weight_map.get(weight, cls.typography.weight_normal)}; "
            f"color: {color_value}; "
            f"line-height: {cls.typography.line_height_text}; "
            f"margin: 0;"
        )
    
    @classmethod
    def get_heading_style(cls, level='h2', color='primary'):
        """
        Generate inline CSS for heading elements.
        
        Args:
            level (str): 'h1', 'h2', 'h3', etc. (not strictly enforced)
            color (str): Color key from Colors class
        
        Returns:
            str: Inline CSS style attribute value
        """
        size_map = {
            'h1': '28px',
            'h2': '24px',
            'h3': '20px',
            'h4': '18px',
        }
        
        color_value = getattr(cls.colors, color, cls.colors.primary)
        
        return (
            f"font-family: {cls.typography.font_primary}; "
            f"font-size: {size_map.get(level, '20px')}; "
            f"font-weight: {cls.typography.weight_bold}; "
            f"color: {color_value}; "
            f"line-height: {cls.typography.line_height_heading}; "
            f"margin: 0 0 16px 0;"
        )
    
    @classmethod
    def get_border_style(cls):
        """
        Generate inline CSS for border/divider.
        
        Returns:
            str: Inline CSS style attribute value
        """
        return f"border: 1px solid {cls.colors.border}; background: {cls.colors.border}; height: 1px; margin: 16px 0;"


# ============================================================================
# SHORTCUTS for common usage
# ============================================================================

# Direct access to colors
COLORS = EmailTheme.colors
TYPOGRAPHY = EmailTheme.typography
COMPONENTS = EmailTheme.components
SPACING = EmailTheme.spacing

# Common color shortcuts
COLOR_PRIMARY = EmailTheme.colors.primary
COLOR_CTA = EmailTheme.colors.cta_bg
COLOR_TEXT = EmailTheme.colors.text
COLOR_MUTED = EmailTheme.colors.muted
COLOR_BORDER = EmailTheme.colors.border


# ============================================================================
# EXAMPLE USAGE IN TEMPLATES
# ============================================================================

"""
# Django template example:

<!-- Simple CTA button -->
<a href="{{ cta_url }}" 
   style="background-color: {{ email_theme.colors.cta_bg }}; 
          color: {{ email_theme.colors.cta_text }}; 
          padding: 12px 24px; 
          border-radius: 6px; 
          text-decoration: none; 
          display: inline-block; 
          font-weight: bold;">
  {{ cta_text }}
</a>

<!-- Text section -->
<p style="font-family: {{ email_theme.typography.font_primary }}; 
          font-size: 16px; 
          color: {{ email_theme.colors.text }}; 
          line-height: 1.6; 
          margin: 0;">
  Newsletter content here
</p>

<!-- Using helper method (Python code) -->
button_style = EmailTheme.get_button_style()
heading_style = EmailTheme.get_heading_style('h2')
text_style = EmailTheme.get_text_style('base', 'normal', 'text')
"""


# ============================================================================
# NOTES FOR IMPLEMENTATION
# ============================================================================

"""
EMAIL-SAFE IMPLEMENTATION CHECKLIST:

✅ Colors: All hex format (no rgba/opacity)
✅ Fonts: Web-safe stacks only (no custom font loading)
✅ Spacing: Pixel-based (rem/em not reliable in email)
✅ Borders: Solid only (no gradients, shadows)
✅ Buttons: Avoid transform/animation (not supported)
✅ Padding: Use <td> cellpadding or inline margin/padding
✅ Images: Always include alt text
✅ Links: Ensure underline on hover (set in client email settings)
✅ Max width: Keep content under 600px (email client standard)
✅ Media queries: Limited support - use sparingly

NOT SUPPORTED IN EMAIL:
❌ rgba/opacity - use solid colors
❌ Custom fonts - use web-safe stacks
❌ box-shadow - use borders instead
❌ transform - no animations/movements
❌ CSS Grid/Flexbox - use tables for layout
❌ rem/em units - use pixels
❌ :hover, :focus - limited support in webmail only
❌ CSS variables - inline all values

TESTING:
- Gmail (webmail & app)
- Outlook.com (webmail)
- Apple Mail (desktop & mobile)
- Thunderbird
- Fallback: Litmus, Email on Acid for preview
"""
