function horizontalLoop(items, config) {
  items = gsap.utils.toArray(items);
  config = config || {};
  const timeline = gsap.timeline({
    repeat: config.repeat,
    paused: config.paused,
    defaults: { ease: "none" },
    onReverseComplete: () =>
      timeline.totalTime(timeline.rawTime() + timeline.duration() * 100),
  });

  const length = items.length;
  const startX = items[0].offsetLeft;
  const times = [];
  const widths = [];
  const xPercents = [];
  let curIndex = 0;

  const pixelsPerSecond = (config.speed || 1) * 100;
  const snap =
    config.snap === false
      ? (value) => value
      : gsap.utils.snap(config.snap || 1);

  gsap.set(items, {
    xPercent: (index, element) => {
      const width = (widths[index] = parseFloat(
        gsap.getProperty(element, "width", "px"),
      ));
      xPercents[index] = snap(
        (parseFloat(gsap.getProperty(element, "x", "px")) / width) * 100 +
          gsap.getProperty(element, "xPercent"),
      );
      return xPercents[index];
    },
  });

  gsap.set(items, { x: 0 });

  const totalWidth =
    items[length - 1].offsetLeft +
    (xPercents[length - 1] / 100) * widths[length - 1] -
    startX +
    items[length - 1].offsetWidth *
      gsap.getProperty(items[length - 1], "scaleX") +
    (parseFloat(config.paddingRight) || 0);

  for (let index = 0; index < length; index++) {
    const item = items[index];
    const curX = (xPercents[index] / 100) * widths[index];
    const distanceToStart = item.offsetLeft + curX - startX;
    const distanceToLoop =
      distanceToStart + widths[index] * gsap.getProperty(item, "scaleX");

    timeline
      .to(
        item,
        {
          xPercent: snap(((curX - distanceToLoop) / widths[index]) * 100),
          duration: distanceToLoop / pixelsPerSecond,
        },
        0,
      )
      .fromTo(
        item,
        {
          xPercent: snap(((curX - distanceToLoop + totalWidth) / widths[index]) * 100),
        },
        {
          xPercent: xPercents[index],
          duration:
            (curX - distanceToLoop + totalWidth - curX) / pixelsPerSecond,
          immediateRender: false,
        },
        distanceToLoop / pixelsPerSecond,
      )
      .add("label" + index, distanceToStart / pixelsPerSecond);

    times[index] = distanceToStart / pixelsPerSecond;
  }

  function toIndex(index, vars) {
    vars = vars || {};

    if (Math.abs(index - curIndex) > length / 2) {
      index += index > curIndex ? -length : length;
    }

    const newIndex = gsap.utils.wrap(0, length, index);
    let time = times[newIndex];

    if ((time > timeline.time()) !== index > curIndex) {
      vars.modifiers = { time: gsap.utils.wrap(0, timeline.duration()) };
      time += timeline.duration() * (index > curIndex ? 1 : -1);
    }

    curIndex = newIndex;
    vars.overwrite = true;
    return timeline.tweenTo(time, vars);
  }

  timeline.next = (vars) => toIndex(curIndex + 1, vars);
  timeline.previous = (vars) => toIndex(curIndex - 1, vars);
  timeline.current = () => curIndex;
  timeline.toIndex = (index, vars) => toIndex(index, vars);
  timeline.times = times;

  timeline.progress(1, true).progress(0, true);

  if (config.reversed) {
    timeline.vars.onReverseComplete();
    timeline.reverse();
  }

  return timeline;
}

document.addEventListener("DOMContentLoaded", () => {
  const root = document.querySelector("[data-carousel-demo]");
  if (!root) return;

  const wrapper = root.querySelector(".about-carousel-wrapper");

  if (!window.gsap || !window.ScrollTrigger) return;
  gsap.registerPlugin(ScrollTrigger);

  const boxes = gsap.utils.toArray(root.querySelectorAll(".about-carousel-box"));
  if (!boxes.length) return;


  const loop = horizontalLoop(boxes, { paused: true, repeat: -1, paddingRight: 16 });
  loop.play();

  const container = root.querySelector(".about-carousel-container");
  if (!container) return;

  ScrollTrigger.create({
    trigger: root,
    start: "top top",
    end: "bottom bottom",
    pin: container,
    onUpdate(self) {
      loop.timeScale(self.direction === -1 ? -1 : 1);
    },
  });
});

