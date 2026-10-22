import React, { useEffect, useRef } from 'react';

/**
 * ButterflyDrift component: creates an ambient drifting butterfly effect in the background
 */
export default function ButterflyDrift() {
  const canvasRef = useRef(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    let animationFrameId;

    const resize = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    };
    resize();
    window.addEventListener('resize', resize);

    const count = 14;
    const butterflies = Array.from({ length: count }, () => ({
      x: Math.random() * canvas.width,
      y: Math.random() * canvas.height,
      size: 10 + Math.random() * 12,
      vx: (Math.random() - 0.5) * 1.2,
      vy: -0.4 - Math.random() * 0.8,
      wingAngle: 0,
      wingSpeed: 0.15 + Math.random() * 0.1,
      hue: Math.random() > 0.5 ? 210 + Math.random() * 40 : 270 + Math.random() * 50,
      alpha: 0.25 + Math.random() * 0.35,
    }));

    const drawButterfly = (b) => {
      ctx.save();
      ctx.translate(b.x, b.y);
      b.wingAngle += b.wingSpeed;
      const wingScale = Math.sin(b.wingAngle);

      ctx.fillStyle = `hsla(${b.hue}, 85%, 65%, ${b.alpha})`;
      ctx.strokeStyle = `hsla(${b.hue}, 90%, 80%, ${b.alpha * 1.2})`;
      ctx.lineWidth = 1;

      // Left wing
      ctx.beginPath();
      ctx.ellipse(-b.size * 0.6 * Math.abs(wingScale), 0, b.size * 0.8 * Math.abs(wingScale), b.size * 0.5, Math.PI / 4, 0, Math.PI * 2);
      ctx.fill();
      ctx.stroke();

      // Right wing
      ctx.beginPath();
      ctx.ellipse(b.size * 0.6 * Math.abs(wingScale), 0, b.size * 0.8 * Math.abs(wingScale), b.size * 0.5, -Math.PI / 4, 0, Math.PI * 2);
      ctx.fill();
      ctx.stroke();

      // Body
      ctx.fillStyle = `rgba(50, 50, 70, ${b.alpha * 0.8})`;
      ctx.fillRect(-1.5, -b.size * 0.4, 3, b.size * 0.8);

      ctx.restore();
    };

    const loop = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      butterflies.forEach((b) => {
        b.x += b.vx + Math.sin(b.wingAngle * 0.3) * 0.5;
        b.y += b.vy;

        // Wrap around borders
        if (b.y < -50) {
          b.y = canvas.height + 30;
          b.x = Math.random() * canvas.width;
        }
        if (b.x < -50) b.x = canvas.width + 30;
        if (b.x > canvas.width + 50) b.x = -30;

        drawButterfly(b);
      });

      animationFrameId = requestAnimationFrame(loop);
    };

    loop();

    return () => {
      cancelAnimationFrame(animationFrameId);
      window.removeEventListener('resize', resize);
    };
  }, []);

  return (
    <canvas
      ref={canvasRef}
      className="fixed inset-0 pointer-events-none z-0 opacity-80"
    />
  );
}
