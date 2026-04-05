# Metallic Swoosh Transition

A premium diagonal shine transition for section changes. Uses crossfade + gradient shine overlay.

**WARNING:** Do NOT use `clipPath` for transitions — it causes black sliver artifacts between scenes.

## Implementation

```tsx
import { TransitionPresentation } from '@remotion/transitions';
import { AbsoluteFill, interpolate } from 'remotion';

export const metallicSwoosh = (): TransitionPresentation => {
  return {
    entering: ({ progress }) => {
      const opacity = interpolate(progress, [0, 0.5, 1], [0, 0.8, 1]);
      return (
        <AbsoluteFill style={{ opacity }}>
          <AbsoluteFill>
            {/* Content */}
            <AbsoluteFill style={{ opacity }}>
              {'<children/>'}
            </AbsoluteFill>
          </AbsoluteFill>
        </AbsoluteFill>
      );
    },
    exiting: ({ progress }) => {
      const opacity = interpolate(progress, [0, 0.5, 1], [1, 0.3, 0]);
      const shinePosition = interpolate(progress, [0, 1], [-200, 120]);

      return (
        <AbsoluteFill>
          {/* Outgoing content fades */}
          <AbsoluteFill style={{ opacity }}>
            {'<children/>'}
          </AbsoluteFill>
          {/* Metallic shine sweeps across */}
          <AbsoluteFill
            style={{
              background: `linear-gradient(
                135deg,
                transparent ${shinePosition - 20}%,
                rgba(255,255,255,0.4) ${shinePosition - 5}%,
                rgba(255,255,255,0.8) ${shinePosition}%,
                rgba(255,255,255,0.4) ${shinePosition + 5}%,
                transparent ${shinePosition + 20}%
              )`,
              pointerEvents: 'none',
            }}
          />
        </AbsoluteFill>
      );
    },
  };
};
```

## Usage

```tsx
import { TransitionSeries } from '@remotion/transitions';
import { metallicSwoosh } from './MetallicSwoosh';

<TransitionSeries>
  <TransitionSeries.Sequence durationInFrames={150}>
    <Scene1 />
  </TransitionSeries.Sequence>
  <TransitionSeries.Transition
    presentation={metallicSwoosh()}
    timing={{ type: 'linear', durationInFrames: 20 }}
  />
  <TransitionSeries.Sequence durationInFrames={150}>
    <Scene2 />
  </TransitionSeries.Sequence>
</TransitionSeries>
```

## Why Not clipPath?

`clipPath` polygon transitions cause a 1px black sliver between exiting and entering scenes due to anti-aliasing. The crossfade + shine approach eliminates this artifact entirely while providing a more premium metallic feel.
