## React Conventions
- Functional component with hooks only.
- If `language = typescript, add explicit prop types and narrow any inferred shapes as needed.
- Do not using `useEffect` unless strictly necessary.

## React File skeleton
- One file exporting **default** page component:
`export default function <Name>Page() {...}`
- Optional small local subcomponents within the same file.

## React Local CSS (only when custom CSS is insufficient)
- Add a `<style>` element **inside** your returned JSX. Example pattern:
```jsx
<style>
`
.nb-local-section { margin-block: 1rem;}
.nb-local-grid {display: grid; gap: 1rem; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));}
`
</style>
```

## React Imports:
- Import only from "react" and "react-router-dom" when needed.
- Use React Router v6+ API (competible with v7) for links:
- Use <Link to="/..."> instead of <a href="/...">