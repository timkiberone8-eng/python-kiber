for (const nav of document.querySelectorAll('[data-lesson-toc]')) {
  const sections = Array.from(nav.querySelectorAll('a[href^="#"]'), link => ({
    link,
    section: document.getElementById(link.hash.slice(1)),
  })).filter(item => item.section);

  if (!sections.length || typeof IntersectionObserver === 'undefined') continue;

  const end = nav.parentElement.querySelector('[data-lesson-end]');
  const page = document.scrollingElement;
  const scrollPosition = () => Math.max(0, Math.min(window.scrollY, page.scrollHeight - page.clientHeight));
  let current;
  let observer;
  let endObserver;
  let atEnd = false;
  let scrollAnchor = scrollPosition();

  function updateVisibility() {
    const y = scrollPosition();
    if (y < 56) {
      nav.removeAttribute('data-shown');
    } else if (Math.abs(y - scrollAnchor) >= 12) {
      nav.toggleAttribute('data-shown', y > scrollAnchor);
    } else {
      return;
    }
    scrollAnchor = y;
  }

  function updateActive(readLine) {
    const visible = atEnd ? sections.at(-1) : sections.findLast(({ section }) =>
      section.getBoundingClientRect().top <= readLine
    ) ?? sections[0];

    if (current === visible) return;
    current?.link.removeAttribute('aria-current');
    visible.link.setAttribute('aria-current', 'location');
    current = visible;
  }

  function observe() {
    observer?.disconnect();
    endObserver?.disconnect();

    const offset = parseFloat(getComputedStyle(sections[0].section).scrollMarginTop) || 0;
    const readLine = Math.min(offset + 4, window.innerHeight - 1);
    observer = new IntersectionObserver(() => updateActive(readLine), {
      rootMargin: `-${readLine}px 0px 0px`,
    });
    for (const { section } of sections) observer.observe(section);

    if (end) {
      endObserver = new IntersectionObserver(([entry]) => {
        atEnd = entry.intersectionRatio === 1;
        updateActive(readLine);
      }, { threshold: 1 });
      endObserver.observe(end);
    }
    updateActive(readLine);
  }

  nav.dataset.ready = '';
  observe();
  window.addEventListener('scroll', updateVisibility, { passive: true });
  window.addEventListener('resize', observe);
}
