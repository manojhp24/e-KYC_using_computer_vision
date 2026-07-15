import { distance } from "../util/math.js";

export class BlinkDetector {
  constructor(threshold = 0.22) {
    this.threshold = threshold;
    this.eyeClosed = false;
    this.blinkCount = 0;
    this.livenessPassed = false;
  }

  calculateEAR(eye, landmarks) {
    const left = landmarks[eye.left];
    const right = landmarks[eye.right];

    const top1 = landmarks[eye.top1];
    const top2 = landmarks[eye.top2];

    const bottom1 = landmarks[eye.bottom1];
    const bottom2 = landmarks[eye.bottom2];

    const vertical1 = distance(top1, bottom1);
    const vertical2 = distance(top2, bottom2);
    const horizontal = distance(left, right);

    return (vertical1 + vertical2) / (2 * horizontal);
  }

  detectBlink(leftEAR, rightEAR) {
    const averageEAR = (leftEAR + rightEAR) / 2;

    if (averageEAR < this.threshold && !this.eyeClosed) {
      this.eyeClosed = true;
    }

    if (averageEAR >= this.threshold && this.eyeClosed) {
      this.eyeClosed = false;
      this.blinkCount++;

      if (this.blinkCount >= 2) {
        this.livenessPassed = true;
      }
    }

    return {
      averageEAR,
      blinkCount: this.blinkCount,
      livenessPassed: this.livenessPassed,
    };
  }

  isLivenessPassed() {
    return this.livenessPassed;
  }

  reset() {
    this.eyeClosed = false;
    this.blinkCount = 0;
    this.livenessPassed = false;
  }
}
