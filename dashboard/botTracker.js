const BotTracker = (() => {
  let data = {
    mouseMoves: 0,
    keyPresses: 0,
    scrolls: 0,
    touches: 0,
    trail: [],
    sessionDuration: 0,
    fingerprint: {}
  };

  function init() {
    document.addEventListener('mousemove', () => data.mouseMoves++);
    document.addEventListener('keydown', () => data.keyPresses++);
    document.addEventListener('scroll', () => data.scrolls++);
    document.addEventListener('touchstart', () => data.touches++);
    setInterval(() => data.sessionDuration++, 1000);
  }

  function getData() {
    return data;
  }

  return { init, getData };
})();