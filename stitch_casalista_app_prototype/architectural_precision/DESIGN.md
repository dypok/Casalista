---
name: Architectural Precision
colors:
  surface: '#faf8ff'
  surface-dim: '#d2d9f4'
  surface-bright: '#faf8ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f2f3ff'
  surface-container: '#eaedff'
  surface-container-high: '#e2e7ff'
  surface-container-highest: '#dae2fd'
  on-surface: '#131b2e'
  on-surface-variant: '#444651'
  inverse-surface: '#283044'
  inverse-on-surface: '#eef0ff'
  outline: '#757682'
  outline-variant: '#c5c5d3'
  surface-tint: '#4059aa'
  primary: '#00236f'
  on-primary: '#ffffff'
  primary-container: '#1e3a8a'
  on-primary-container: '#90a8ff'
  inverse-primary: '#b6c4ff'
  secondary: '#0051d5'
  on-secondary: '#ffffff'
  secondary-container: '#316bf3'
  on-secondary-container: '#fefcff'
  tertiary: '#1d2b3a'
  on-tertiary: '#ffffff'
  tertiary-container: '#334151'
  on-tertiary-container: '#9eadc0'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#dce1ff'
  primary-fixed-dim: '#b6c4ff'
  on-primary-fixed: '#00164e'
  on-primary-fixed-variant: '#264191'
  secondary-fixed: '#dbe1ff'
  secondary-fixed-dim: '#b4c5ff'
  on-secondary-fixed: '#00174b'
  on-secondary-fixed-variant: '#003ea8'
  tertiary-fixed: '#d5e4f8'
  tertiary-fixed-dim: '#b9c8db'
  on-tertiary-fixed: '#0e1d2b'
  on-tertiary-fixed-variant: '#3a4858'
  background: '#faf8ff'
  on-background: '#131b2e'
  surface-variant: '#dae2fd'
typography:
  display-currency:
    fontFamily: Manrope
    fontSize: 32px
    fontWeight: '800'
    lineHeight: 38px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Manrope
    fontSize: 24px
    fontWeight: '700'
    lineHeight: 30px
    letterSpacing: -0.015em
  headline-md:
    fontFamily: Manrope
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 26px
    letterSpacing: -0.01em
  headline-sm:
    fontFamily: Manrope
    fontSize: 16px
    fontWeight: '600'
    lineHeight: 22px
    letterSpacing: 0em
  body-lg:
    fontFamily: Hanken Grotesk
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
    letterSpacing: 0em
  body-md:
    fontFamily: Hanken Grotesk
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
    letterSpacing: 0em
  body-sm:
    fontFamily: Hanken Grotesk
    fontSize: 12px
    fontWeight: '400'
    lineHeight: 16px
    letterSpacing: 0.01em
  label-lg:
    fontFamily: Hanken Grotesk
    fontSize: 14px
    fontWeight: '600'
    lineHeight: 18px
    letterSpacing: 0.01em
  label-md:
    fontFamily: Hanken Grotesk
    fontSize: 12px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.02em
  label-sm:
    fontFamily: Hanken Grotesk
    fontSize: 10px
    fontWeight: '700'
    lineHeight: 12px
    letterSpacing: 0.04em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  gutter: 1rem
  margin: 1rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 1rem
  space-lg: 1.5rem
  space-xl: 2rem
---

## Brand & Style

This design system establishes an architectural and institutional framework tailored for residential financial planning, construction scopes, and home maintenance budgeting. Rooted in structural clarity, it balances the fiscal authority of deep navy tones with pragmatic operational utility. 

The aesthetic is functional minimalism: high-contrast legibility, metric-first data displays, tactile containment, and zero decorative noise. Designed for homeowners and contractors navigating financial estimations in Colombian Pesos (COP), the visual tone communicates mathematical precision, stability, and transparency. Surfaces remain crisp and planar, employing subtle borders and micro-elevations to organize complex material costs, labor fees, and project workflows seamlessly within focused mobile viewports.

## Colors

The color system prioritizes visual hierarchy and financial clarity through a deliberate balance of authoritative navies, active task blues, and neutral scaffolding:

- **Primary (`#1E3A8A`)**: Serves as the bedrock of structural trust. Used for top app bars, primary section headers, critical total sums, navigation anchors, and dominant interactive containers.
- **Secondary (`#2563EB`)**: Signals interactive agency and workflow progress. Applied to primary CTAs, active toggles, input selection states, and interactive calculation steppers.
- **Tertiary & Tint (`#DBEAFE`)**: Used for soft card highlights, selected row fills, contextual badge backgrounds, and secondary interactive chip states.
- **Neutral Canvas & Surfaces**:
  - `Surface Base`: `#FFFFFF` for primary cards and canvas baseline.
  - `Surface Subtle`: `#F8FAFC` for scaffold backgrounds, grouping trays, and disabled card states.
  - `Text Primary`: `#0F172A` providing optimal contrast for numbers and financial breakdowns.
  - `Text Secondary / Muted`: `#64748B` for unit measures, field labels, metadata, and COP denomination indicators.
  - `Borders & Rules`: `#E2E8F0` for structural gridlines, card borders, and list dividers.
- **Functional Semantics**:
  - `Success`: `#16A34A` text/icon on `#DCFCE7` fill for approved estimates and settled budgets.
  - `Warning`: `#CA8A04` text/icon on `#FEF9C3` fill for budget thresholds reaching 85-95%.
  - `Danger / Alert`: `#DC2626` text/icon on `#FEE2E2` fill for budget overruns and critical repair dependencies.

## Typography

Typography pairs the structural, geometric presence of **Manrope** for authoritative headlines and currency values with the legible, functional efficiency of **Hanken Grotesk** for operational content and micro-copy:

- **Currency & Metric Stacking**: For COP amounts (e.g., `$1.450.000`), always use tabular figures with `display-currency` or `headline-lg` in Manrope, ensuring currency symbols (`$`) and ISO labels (`COP`) scale down one typographic step to preserve numerical prominence.
- **Hierarchy Rules**:
  - `Manrope` is strictly reserved for titles, section headings, card headers, and financial totalizers.
  - `Hanken Grotesk` drives all reading contexts, field indicators, tables of materials, and interactive states.
- **Mobile Readability Safeguards**: Base text does not drop below 12px for informative copy. 10px uppercase tracking is limited solely to technical metadata chips and status pills.

## Layout & Spacing

The layout is optimized for single-hand mobile operation centered on a standard 390px viewport width:

- **Grid Architecture**: Single-column flexible fluid card stack bounded by a standard outer canvas margin of `16px` (`margin: 1rem`) and grid column gutters of `16px` (`gutter: 1rem`).
- **Vertical Spacing Rhythm**: Built on an absolute 4px/8px incremental scale:
  - `space-xs (4px)`: Micro-padding between badge icons and text; input label-to-control distance.
  - `space-sm (8px)`: Spacing between closely grouped list sub-items and segmented pill tabs.
  - `space-md (16px)`: Standard component inner padding for cards, form fields, and modal containers.
  - `space-lg (24px)`: Vertical rhythm separating structural blocks and budget categories.
  - `space-xl (32px)`: Spacing preceding major section divisions and bottom-sheet anchors.
- **Safe Zones & Reachability**: Critical CTAs and primary budget calculation summaries reside within a sticky bottom viewport tray padded with `16px` lateral margins and bottom safe-area insets.

## Elevation & Depth

Depth is established through crisp surface layering and low-contrast borders rather than deep dramatic drop shadows, maintaining an architectural, plan-drawing aesthetic:

- **Base Layer (Level 0)**: `#F8FAFC` canvas scaffold.
- **Contained Layer (Level 1)**: Flat `#FFFFFF` surface containers delineated by a 1px solid `#E2E8F0` border. Zero shadow for inert cards.
- **Elevated Interactive Layer (Level 2)**: Used for active interactive cards, summary banners, and sticky budget tallies. Achieved via `border: 1px solid #E2E8F0` coupled with an ambient shadow: `box-shadow: 0 1px 3px 0 rgba(15, 23, 42, 0.05), 0 1px 2px -1px rgba(15, 23, 42, 0.05)`.
- **Overlay & Sheets (Level 3)**: Modals, calculation drawers, and bottom action sheets use `#FFFFFF` with a 1px border on top and `box-shadow: 0 10px 15px -3px rgba(15, 23, 42, 0.08), 0 4px 6px -4px rgba(15, 23, 42, 0.03)` with a neutral backdrop dim of `rgba(15, 23, 42, 0.4)`.

## Shapes

The shape system employs roundedness index `2`, delivering balanced radii across components:

- **Base Corner Radius (0.5rem / 8px)**: Inputs, small interactive chips, quantity step adjusters, and status badges.
- **Large Corner Radius (`rounded-lg` - 1rem / 16px)**: Primary cards, calculation metric containers, inspection modules, and bottom sheet tops.
- **Extra Large Radius (`rounded-xl` - 1.5rem / 24px)**: Primary operational buttons, persistent floating estimate counters, and bottom navigation docking capsules.
- **Structural Integrity**: Outlines remain strictly 1px with no offset interior rings, keeping financial summaries structured and legible.

## Components

### Buttons
- **Primary Action**: Solid `#2563EB` fill, `#FFFFFF` text, `12px` vertical padding, `rounded-xl` (16px), semibold 14px Hanken Grotesk. Active state dims to `#1E3A8A`.
- **Secondary / Technical**: `#FFFFFF` background, `1px solid #E2E8F0`, `#0F172A` text.
- **Destructive**: Solid `#FEE2E2` fill, `#DC2626` text, with transition to `#DC2626` fill and `#FFFFFF` text upon confirmation.

### Budget Cards & Metric Blocks
- Background `#FFFFFF`, border `1px solid #E2E8F0`, corner radius `16px`, padding `16px`.
- Visual partition: Upper quadrant holds category header and icon (e.g., "Pintura y Acabados"); center houses prominent Manrope tabular currency balance in `#0F172A`; lower tray uses `#F8FAFC` background with status badge and material/labor percentage splits.

### Inputs & Quantity Steppers
- Height `48px`, `#FFFFFF` surface, `1px solid #E2E8F0`, radius `8px`, placeholder `#64748B`.
- Focused state: Border changes to `#2563EB` with an inline badge denoting `COP`.
- Numeric steppers (e.g., m², hours of labor) feature integrated left/right decrement/increment tap targets in `#F8FAFC` with `#1E3A8A` iconography.

### Chips & Filters
- Compact horizontal scroll grouping. Height `32px`, corner radius `8px`.
- Inactive: `#FFFFFF` fill, `#E2E8F0` border, `#64748B` text.
- Active: `#DBEAFE` fill, `#2563EB` border, `#1E3A8A` semibold text.

### Selection Controls (Checkboxes & Radios)
- Checkboxes: `20x20px`, `rounded` (4px). Unchecked: `1px solid #E2E8F0`. Checked: `#2563EB` fill with white checkmark.
- Radio buttons: Circular 20px target for selecting repair material quality (Económico, Estándar, Premium). Active state shows an outer `#2563EB` ring with a 6px central core.

### Lists & Breakdown Rows
- Flush edge-to-edge separation with `#E2E8F0` dividing rules.
- 3-column financial distribution: Task/Material name left-aligned (`#0F172A`), sub-detail unit cost below (`#64748B`), and aggregate sum right-aligned in tabular bold Manrope.