# UI Preview

## Desktop View

```
┌────────────────────────────────────────────────────────────────┐
│  ✨ AI Chat                                    🟢 Online       │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│                                                                 │
│                                                                 │
│   🤖  AI Assistant                              10:30 PM       │
│   ┌─────────────────────────────────────────────────┐          │
│   │ Hello! How can I help you today?                │          │
│   └─────────────────────────────────────────────────┘          │
│                                                                 │
│                                                                 │
│                                          👤  You   10:31 PM    │
│          ┌─────────────────────────────────────────────────┐   │
│          │ What is artificial intelligence?                │   │
│          └─────────────────────────────────────────────────┘   │
│                                                                 │
│                                                                 │
│   🤖  AI Assistant                              10:31 PM       │
│   ┌─────────────────────────────────────────────────┐          │
│   │ Artificial Intelligence (AI) refers to the      │          │
│   │ simulation of human intelligence in machines... │          │
│   └─────────────────────────────────────────────────┘          │
│                                                                 │
│                                                                 │
│   🤖  AI is thinking...                                        │
│   ┌─────────────────┐                                          │
│   │ ● ● ●           │  (animated dots)                         │
│   └─────────────────┘                                          │
│                                                                 │
├────────────────────────────────────────────────────────────────┤
│  ┌──────────────────────────────────────────────────────┐  ➤  │
│  │ Type your message...                                 │ [●] │
│  └──────────────────────────────────────────────────────┘     │
│     Press Enter to send, Shift + Enter for new line           │
└────────────────────────────────────────────────────────────────┘
```

## Color Scheme

- **Background**: Very dark (#0a0a0f → #13131a gradient)
- **Glass Elements**: Frosted glass with blur (rgba(255,255,255,0.05))
- **Accent**: Purple-blue gradient (#6366f1 → #8b5cf6)
- **Text**: White (#ffffff) and gray (#a1a1aa)
- **Borders**: Subtle white (rgba(255,255,255,0.1))

## Key Visual Features

### Header
- Glassmorphism effect with backdrop blur
- Gradient logo text
- Animated floating sparkle icon
- Pulsing green status dot

### Messages
- **AI Messages** (Left):
  - Robot emoji avatar in glass circle
  - Dark glass bubble background
  - Hover effect: slightly lighter
  
- **User Messages** (Right):
  - User emoji avatar in gradient circle
  - Purple gradient bubble background
  - Glow shadow effect
  - Hover effect: lift up slightly

### Animations
- Messages slide in from bottom with fade
- Loading dots bounce up and down
- Send button rotates on hover
- Status dot pulses
- Logo icon floats up and down

### Input Area
- Large rounded input box
- Circular gradient send button
- Disabled state shows loading spinner
- Focus state: blue glow around input

## Responsive Design

### Mobile (< 768px)
- Smaller avatars (36px instead of 40px)
- Messages take 85% width instead of 70%
- Reduced padding
- Status text hidden
- Smaller font sizes

## Accessibility
- Semantic HTML structure
- Keyboard navigation (Enter, Shift+Enter)
- Focus indicators
- Color contrast ratios met
- Screen reader friendly (can be improved)

## Micro-interactions
1. **Message send**: Input clears, loading appears, message slides in
2. **Hover effects**: Buttons scale, messages lift, colors brighten
3. **Auto-scroll**: Smooth scroll to latest message
4. **Loading state**: Animated bouncing dots
5. **Button press**: Scale down on click
