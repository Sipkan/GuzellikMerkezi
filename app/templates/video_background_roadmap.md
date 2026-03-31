# 🎬 Video Background Hero Section — Learning Roadmap

A step-by-step guide to adding a background video to your `<section class="hero">` on the home page.

---

## 📐 The Core Concept: Layered Stacking

The entire technique relies on **stacking 3 layers** inside one container using CSS positioning:

```
z-index: 2  →  🔤 Text content    (hero-content)
z-index: 1  →  ⬛ Dark overlay    (hero-overlay)
z-index: 0  →  🎬 Video           (hero-bg-video)
```

> You already use this exact pattern in your `service_detail.html` with the `.service-hero-video` class (lines 395–437 in `style.css`).

---

## Step 1 — Update the HTML

**Before:**

```html
<section class="hero">
  <h1>Pınar Seda Sayan Güzellik Dünyası</h1>
  <p>Mutluluğunuzun ve güzelliğinizin daimi noktası</p>
</section>
```

**After:**

```html
<section class="hero">
  <!-- Layer 0: Background video -->
  <video autoplay muted loop playsinline class="hero-bg-video">
    <source src="/static/videos/your-video.mp4" type="video/mp4" />
  </video>

  <!-- Layer 1: Dark overlay for text readability -->
  <div class="hero-overlay"></div>

  <!-- Layer 2: Your content on top -->
  <div class="hero-content">
    <h1>Pınar Seda Sayan Güzellik Dünyası</h1>
    <p>Mutluluğunuzun ve güzelliğinizin daimi noktası</p>
  </div>
</section>
```

### `<video>` Attributes Explained

| Attribute     | What it does                                                       |
| ------------- | ------------------------------------------------------------------ |
| `autoplay`    | Starts playing automatically when the page loads                   |
| `muted`       | Silences the audio — **required** by browsers for autoplay to work |
| `loop`        | When the video ends, it restarts from the beginning automatically  |
| `playsinline` | On iOS, prevents the video from going fullscreen when it plays     |

---

## Step 2 — CSS: The Container (`.hero`)

```css
.hero {
  position: relative;
  overflow: hidden;
  text-align: center;
  padding: 4rem 2rem;
  border-radius: 8px;
  margin-bottom: 2rem;
}
```

### Property Explanations

| Property             | What it does                                                                                                                                                                              | Why we need it                                                                           |
| -------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| `position: relative` | Makes this element the **reference point** for any `position: absolute` children inside it. Without this, absolute children would position themselves relative to the whole page instead. | The video and overlay need to be positioned relative to _this section_, not the page.    |
| `overflow: hidden`   | Anything that sticks out beyond this box's edges gets **clipped** (hidden).                                                                                                               | The video is often larger than the section — this cuts off the excess so it looks clean. |
| `text-align: center` | Centers inline content (text, inline elements) horizontally.                                                                                                                              | Centers the `<h1>` and `<p>` text.                                                       |
| `padding: 4rem 2rem` | Adds **inner space** — `4rem` top/bottom, `2rem` left/right. `1rem` = 16px by default.                                                                                                    | Creates breathing room around the text content.                                          |
| `border-radius: 8px` | Rounds the corners of the box by 8 pixels.                                                                                                                                                | Aesthetic choice — makes the section look softer.                                        |

---

## Step 3 — CSS: The Video (`.hero-bg-video`)

```css
.hero-bg-video {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  min-width: 100%;
  min-height: 100%;
  object-fit: cover;
  z-index: 0;
}
```

### Property Explanations

| Property                           | What it does                                                                                                                                                          | Why we need it                                                                                                                                                     |
| ---------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `position: absolute`               | **Removes** the element from the normal document flow. It no longer takes up space. Instead, it positions itself relative to the nearest `position: relative` parent. | We want the video to sit _behind_ the content, not push it down. It should float freely inside the section.                                                        |
| `top: 50%; left: 50%`              | Moves the video's **top-left corner** to the exact center of the parent.                                                                                              | First half of the centering trick — but now the video is off-center because its top-left corner is at center, not its middle.                                      |
| `transform: translate(-50%, -50%)` | Shifts the element back by **50% of its own width and height**.                                                                                                       | This corrects the offset from `top/left: 50%`, making the video's **center** align with the parent's center. Together, these 3 properties = **perfect centering**. |
| `min-width: 100%`                  | The video must be **at least** as wide as the parent. It can be wider, but never narrower.                                                                            | Ensures no gaps appear on the sides, regardless of the video's aspect ratio.                                                                                       |
| `min-height: 100%`                 | The video must be **at least** as tall as the parent.                                                                                                                 | Ensures no gaps appear on the top/bottom.                                                                                                                          |
| `object-fit: cover`                | Scales & crops the video to **fill** the box while maintaining aspect ratio. Like a photo being cropped to fit a frame.                                               | Without this, the video might stretch/distort. `cover` = always fills, may crop edges.                                                                             |
| `z-index: 0`                       | Sets the **stacking order**. Lower values go behind, higher values go in front.                                                                                       | Puts the video at the very back layer (behind overlay and text).                                                                                                   |

### 🔑 The Centering Trick Visualized

```
Step 1: top: 50%; left: 50%
┌──────────────────────┐
│         parent       │
│          ↓           │
│          ┌───────┐   │   ← video's top-left corner is at center
│          │ VIDEO │   │
│          └───────┘   │
└──────────────────────┘

Step 2: transform: translate(-50%, -50%)
┌──────────────────────┐
│      ┌───────┐       │
│      │ VIDEO │       │   ← video's CENTER is now at center ✓
│      └───────┘       │
└──────────────────────┘
```

---

## Step 4 — CSS: The Overlay (`.hero-overlay`)

```css
.hero-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.4);
  z-index: 1;
}
```

### Property Explanations

| Property                         | What it does                                                                                                          | Why we need it                                                                                                   |
| -------------------------------- | --------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| `position: absolute`             | Same as the video — removes from flow, positions relative to parent.                                                  | We want it to cover the entire section without affecting layout.                                                 |
| `top: 0; left: 0`                | Pins the overlay's top-left corner to the parent's top-left corner.                                                   | Together with `width/height: 100%`, this makes the overlay cover the entire section exactly.                     |
| `width: 100%; height: 100%`      | Stretches to fill the parent completely.                                                                              | Creates a full-coverage tint over the video.                                                                     |
| `background: rgba(0, 0, 0, 0.4)` | Sets a **semi-transparent black** background. `rgba` = Red, Green, Blue, Alpha. `0,0,0` = black. `0.4` = 40% opacity. | Darkens the video so white text is readable on top. Increase to `0.6` for darker, decrease to `0.2` for lighter. |
| `z-index: 1`                     | Stacking order = 1.                                                                                                   | Sits above the video (0) but below the text content (2).                                                         |

### 🎨 Understanding `rgba()`

```
rgba(  0,   0,   0,  0.4  )
       │    │    │    │
       │    │    │    └─ Alpha (opacity): 0 = invisible, 1 = fully solid
       │    │    └────── Blue:  0-255
       │    └─────────── Green: 0-255
       └──────────────── Red:   0-255

Examples:
  rgba(0, 0, 0, 0.4)       = 40% black  (light tint)
  rgba(0, 0, 0, 0.7)       = 70% black  (heavy tint)
  rgba(255, 255, 255, 0.3)  = 30% white  (frosted glass effect)
```

---

## Step 5 — CSS: The Content (`.hero-content`)

```css
.hero-content {
  position: relative;
  z-index: 2;
}

.hero-content h1 {
  font-size: 2.5rem;
  color: #fff;
  text-shadow: 0 2px 8px rgba(0, 0, 0, 0.5);
}

.hero-content p {
  color: #e8d5c4;
}
```

### Property Explanations

| Property                                 | What it does                                                                                                                                                                 | Why we need it                                                                                     |
| ---------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| `position: relative`                     | Unlike `absolute`, this keeps the element **in the normal flow** (it still takes up space). But it **activates `z-index`** — without a position value, `z-index` is ignored! | We need `z-index` to bring the text in front, but we don't want to remove it from the layout flow. |
| `z-index: 2`                             | Highest layer.                                                                                                                                                               | Text appears above both the video (0) and overlay (1).                                             |
| `text-shadow: 0 2px 8px rgba(0,0,0,0.5)` | Adds a soft shadow behind the text. Values: `horizontal-offset`, `vertical-offset`, `blur-radius`, `color`.                                                                  | Extra readability boost — gives text a subtle glow against the video.                              |

### 💡 `position: relative` vs `position: absolute`

```
position: relative
  ✓ Element STAYS in normal flow (takes up space)
  ✓ Can use z-index
  ✓ Can nudge with top/left (offset from its normal position)

position: absolute
  ✗ Element is REMOVED from normal flow (takes up NO space)
  ✓ Can use z-index
  ✓ Positions relative to nearest positioned ancestor
  → Used for: videos, overlays, floating elements
```

---

## Step 6 — Optional Enhancements

### Poster image (fallback while video loads)

```html
<video
  autoplay
  muted
  loop
  playsinline
  class="hero-bg-video"
  poster="/static/images/hero-poster.jpg"
></video>
```

`poster` = a static image displayed while the video is loading or if the browser can't play it.

### Gradient overlay instead of solid color

```css
.hero-overlay {
  background: linear-gradient(
    to bottom,
    rgba(0, 0, 0, 0.2) 0%,
    rgba(0, 0, 0, 0.6) 100%
  );
}
```

`linear-gradient(to bottom, ...)` = fades from light at top to dark at bottom. Makes the bottom text area more readable while keeping the top of the video visible.

### Slow-motion playback

```javascript
document.querySelector(".hero-bg-video").playbackRate = 0.75;
```

`playbackRate` = speed multiplier. `0.75` = 75% speed (slight slow motion), `0.5` = half speed.

---

## ⚠️ Performance Tips

| Tip                                              | Why                                                              |
| ------------------------------------------------ | ---------------------------------------------------------------- |
| Keep video under **5–10 MB**                     | Larger files = slow page load, bad mobile experience             |
| Use **720p** resolution max                      | Higher res adds file size but won't look better in a background  |
| Make it **10–15 seconds** long                   | Longer = bigger file. Short loops look seamless                  |
| Compress with [HandBrake](https://handbrake.fr/) | Free tool to reduce video file size without visible quality loss |

---

## ✅ Checklist

- [x] Video file placed in `app/static/videos/`
- [ ] Video compressed to under 10 MB
- [x] HTML updated with `<video>`, overlay `<div>`, and content wrapper
- [x] `.index-hero` CSS updated with `position: relative` and `overflow: hidden`
- [x] Old `background: linear-gradient(...)` removed
- [x] `.hero-index-bg-video` CSS added
- [ ] Overlay CSS added (`.hero-index-bg-video-overlay`)
- [ ] Content CSS added with `z-index: 2` (`.hero-index-bg-video-content`)
- [ ] Text colors updated for readability on dark background
- [ ] Tested on both desktop and mobile
