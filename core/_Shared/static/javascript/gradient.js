class GradientColor {
    constructor() {
        this.minNum = 0;
        this.maxNum = 10;
        this.startHex = "";
        this.endHex = "";
    }

    setColorGradient(colorStart, colorEnd) {
        if (!colorStart.startsWith("#") || !colorEnd.startsWith("#")) {
            throw new Error('Colors must be in hexadecimal format starting with "#"');
        }
        this.startHex = this.#expandHex(colorStart);
        this.endHex = this.#expandHex(colorEnd);
    }

    #expandHex(hex) {
        if (hex.length === 4) {
            return (
                "#" +
                hex[1] + hex[1] +
                hex[2] + hex[2] +
                hex[3] + hex[3]
            );
        } else if (hex.length === 7) {
            return hex;
        }
        throw new Error(
            "Invalid color format. Use #RRGGBB or #RGB (e.g., #3f2caf)."
        );
    }

    setRange(minNumber = 0, maxNumber = 10) {
        this.minNum = minNumber;
        this.maxNum = maxNumber;
    }

    getColor(numberValue) {
        if (numberValue === undefined) return undefined;
        return (
            "#" +
            this.#lerpHex(numberValue, this.startHex.substring(1, 3), this.endHex.substring(1, 3)) +
            this.#lerpHex(numberValue, this.startHex.substring(3, 5), this.endHex.substring(3, 5)) +
            this.#lerpHex(numberValue, this.startHex.substring(5, 7), this.endHex.substring(5, 7))
        );
    }

    #lerpHex(number, start, end) {
        const n = Math.min(Math.max(number, this.minNum), this.maxNum);
        const span = this.maxNum - this.minNum || 1; // avoid /0
        const a = parseInt(start, 16);
        const b = parseInt(end, 16);
        const v = Math.round(((b - a) / span) * (n - this.minNum) + a);
        return v.toString(16).padStart(2, "0");
    }
}

class Gradient {
    constructor() {
        this.size = 10;          // number of steps (e.g., text length)
        this.colors = [];        // array of hex colors
        this.stops = [];         // array of positions [0..1], same length as colors
        this._segments = [];     // [{range:[lo,hi], lerp:GradientColor}]
    }

    /**
     * colors: array of "#RRGGBB"
     * stops:  array of numbers in [0,1] (same length as colors). If omitted, evenly spaced.
     */
    setGradient(colors, stops) {
        if (!Array.isArray(colors) || colors.length < 2) {
            throw new RangeError("Provide at least 2 colors.");
        }

        // default evenly spaced stops
        if (!stops) {
            stops = colors.map((_, i) => (colors.length === 1 ? 0 : i / (colors.length - 1)));
        }

        if (stops.length !== colors.length) {
            throw new RangeError("stops must match colors length.");
        }

        // validate stops [0..1], increasing, first=0 last=1 (we’ll coerce softly)
        stops = stops
            .map((s) => Math.min(1, Math.max(0, Number(s))))
            .sort((a, b) => a - b);

        if (stops[0] !== 0) stops[0] = 0;
        if (stops[stops.length - 1] !== 1) stops[stops.length - 1] = 1;

        this.colors = colors.slice();
        this.stops = stops.slice();
        this.#rebuildSegments();
        return this;
    }

    setSize(n) {
        const v = Math.max(1, Math.floor(Number(n)));
        this.size = v;
        this.#rebuildSegments();
        return this;
    }

    #rebuildSegments() {
        if (this.colors.length < 2) return;

        const steps = Math.max(1, this.size - 1); // indices 0..(size-1)
        this._segments = [];

        for (let i = 0; i < this.colors.length - 1; i++) {
            const aStop = Math.round(this.stops[i] * steps);
            const bStop = Math.round(this.stops[i + 1] * steps);
            const lo = Math.min(aStop, bStop);
            const hi = Math.max(aStop, bStop);

            const g = new GradientColor();
            g.setColorGradient(this.colors[i], this.colors[i + 1]);
            g.setRange(lo, hi);

            this._segments.push({ range: [lo, hi], lerp: g });
        }
    }

    getColor(idx) {
        if (isNaN(idx)) throw new TypeError("getColor requires a numeric index.");
        const i = Math.min(Math.max(0, Math.floor(idx)), this.size - 1);

        // find segment containing i (inclusive at end so last index hits last color)
        const seg = this._segments.find(({ range: [lo, hi] }) => i >= lo && i <= hi);
        if (!seg) {
            // if gaps occur (equal stops), fall back to nearest color by stop
            const nearest = this.#nearestStopIndex(i);
            return this.colors[nearest];
        }
        return seg.lerp.getColor(i);
    }

    getColors() {
        const out = [];
        for (let i = 0; i < this.size; i++) out.push(this.getColor(i));
        return out;
    }

    #nearestStopIndex(i) {
        const steps = Math.max(1, this.size - 1);
        let best = 0;
        let bestDist = Infinity;
        for (let k = 0; k < this.stops.length; k++) {
            const pos = Math.round(this.stops[k] * steps);
            const d = Math.abs(pos - i);
            if (d < bestDist) {
                bestDist = d;
                best = k;
            }
        }
        return best;
    }
}