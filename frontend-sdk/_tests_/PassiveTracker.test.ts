import { PassiveTracker } from "../PassiveTracker";

describe("PassiveTracker", () => {
  it("should initialize and expose startTracking", () => {
    const tracker = PassiveTracker();
    expect(typeof tracker.startTracking).toBe("function");
  });
});