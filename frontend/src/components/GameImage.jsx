import React, { useState, useEffect } from 'react';
import { Gamepad2 } from 'lucide-react';

export default function GameImage({
  src,
  alt = 'Game cover',
  className = 'w-full h-full object-cover',
  containerClassName = '',
  iconSize = 'w-8 h-8',
}) {
  const [hasError, setHasError] = useState(false);

  useEffect(() => {
    setHasError(false);
  }, [src]);

  const isValidUrl = src && typeof src === 'string' && src.trim().length > 0 && !src.includes('placeholder.com');

  if (!isValidUrl || hasError) {
    return (
      <div
        className={`bg-zinc-950 flex flex-col items-center justify-center text-zinc-500 select-none overflow-hidden ${containerClassName}`}
        title={alt}
      >
        <Gamepad2 className={`${iconSize} text-zinc-600 stroke-1 mb-1`} />
        <span className="text-[10px] text-zinc-500 font-mono tracking-wider uppercase text-center px-1 truncate max-w-full">
          No Cover
        </span>
      </div>
    );
  }

  return (
    <img
      src={src}
      alt={alt}
      className={className}
      loading="lazy"
      onError={() => setHasError(true)}
    />
  );
}
