import React from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Badge } from '@/components/ui/badge';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import { AlertCircle } from 'lucide-react';

interface ComponentProps {
  element: any;
  tokens?: any;
}

/**
 * DYNAMIC COMPONENT RENDERER
 * Renders ANY component from LLM JSON response
 * NO HARDCODING - 100% data-driven
 */
export const DynamicComponent: React.FC<ComponentProps> = ({ element, tokens }) => {
  if (!element) return null;

  const getColor = (colorRef?: string): string => {
    if (!colorRef) return '#000000';
    if (colorRef.startsWith('#')) return colorRef;
    if (colorRef.startsWith('rgb')) return colorRef;
    return tokens?.colors?.[colorRef] || colorRef || '#000000';
  };

  const getSpacing = (spacingRef?: string | number): number => {
    if (typeof spacingRef === 'number') return spacingRef;
    if (!spacingRef) return 0;
    const spacingValue = tokens?.spacing?.[spacingRef];
    if (spacingValue) return spacingValue;
    return parseInt(spacingRef as string) || 0;
  };

  const baseStyle: React.CSSProperties = {
    position: 'absolute',
    left: element.x || 0,
    top: element.y || 0,
    width: element.width || 'auto',
    height: element.height || 'auto',
  };

  // ============ TEXT ============
  if (element.type === 'text' || element.type === 'paragraph') {
    return (
      <div
        style={{
          ...baseStyle,
          fontSize: element.fontSize || 16,
          fontWeight: element.fontWeight || 'normal',
          color: getColor(element.color),
          padding: getSpacing(element.padding),
          lineHeight: element.lineHeight || 1.5,
          whiteSpace: 'pre-wrap',
          wordWrap: 'break-word',
        }}
      >
        {element.content || element.label || 'Text'}
      </div>
    );
  }

  // ============ HEADING ============
  if (element.type === 'heading') {
    const HeadingTag = (element.level === 2 ? 'h2' : element.level === 3 ? 'h3' : 'h1') as keyof JSX.IntrinsicElements;
    return (
      <HeadingTag
        style={{
          ...baseStyle,
          fontSize: element.fontSize || 24,
          fontWeight: element.fontWeight || 'bold',
          color: getColor(element.color),
          padding: getSpacing(element.padding),
          margin: 0,
          lineHeight: 1.2,
        }}
      >
        {element.content || element.label || 'Heading'}
      </HeadingTag>
    );
  }

  // ============ BUTTON ============
  if (element.type === 'button') {
    return (
      <Button
        style={{
          position: 'absolute',
          left: element.x,
          top: element.y,
          width: element.width,
          height: element.height,
          backgroundColor: getColor(element.background),
          color: getColor(element.color),
          fontSize: element.fontSize || 14,
          fontWeight: element.fontWeight || 500,
          borderRadius: element.borderRadius || 6,
        }}
        variant={element.variant || 'default'}
      >
        {element.label || element.content || 'Button'}
      </Button>
    );
  }

  // ============ INPUT ============
  if (element.type === 'input') {
    return (
      <div
        style={{
          position: 'absolute',
          left: element.x,
          top: element.y,
          width: element.width,
          height: 'auto',
        }}
      >
        {element.label && (
          <Label style={{ display: 'block', marginBottom: 8, fontWeight: 500 }}>
            {element.label}
          </Label>
        )}
        <Input
          type={element.inputType || 'text'}
          placeholder={element.placeholder || 'Enter text...'}
          style={{
            width: '100%',
            padding: `${getSpacing(element.padding || 8)}px`,
            backgroundColor: getColor(element.background),
            color: getColor(element.color),
            borderRadius: element.borderRadius || 6,
            fontSize: element.fontSize || 14,
          }}
        />
      </div>
    );
  }

  // ============ TEXTAREA ============
  if (element.type === 'textarea') {
    return (
      <div
        style={{
          position: 'absolute',
          left: element.x,
          top: element.y,
          width: element.width,
          height: 'auto',
        }}
      >
        {element.label && (
          <Label style={{ display: 'block', marginBottom: 8 }}>
            {element.label}
          </Label>
        )}
        <textarea
          placeholder={element.placeholder || 'Enter text...'}
          style={{
            width: '100%',
            minHeight: element.height || 100,
            padding: `${getSpacing(element.padding || 8)}px`,
            backgroundColor: getColor(element.background),
            color: getColor(element.color),
            borderRadius: element.borderRadius || 6,
            fontSize: element.fontSize || 14,
            border: '1px solid #e5e7eb',
            fontFamily: 'inherit',
            resize: 'vertical',
          }}
        />
      </div>
    );
  }

  // ============ CARD ============
  if (element.type === 'card') {
    return (
      <Card
        style={{
          position: 'absolute',
          left: element.x,
          top: element.y,
          width: element.width,
          height: element.height,
          backgroundColor: getColor(element.background),
          borderRadius: element.borderRadius || 8,
        }}
      >
        {element.title && (
          <CardHeader>
            <CardTitle style={{ color: getColor(element.titleColor) }}>
              {element.title}
            </CardTitle>
            {element.description && (
              <CardDescription>{element.description}</CardDescription>
            )}
          </CardHeader>
        )}
        <CardContent>
          {element.children && element.children.length > 0 ? (
            <div style={{ position: 'relative', width: '100%', height: '100%' }}>
              {element.children.map((child: any, idx: number) => (
                <DynamicComponent
                  key={`${element.id}-child-${idx}`}
                  element={child}
                  tokens={tokens}
                />
              ))}
            </div>
          ) : (
            <p style={{ color: getColor(element.color) }}>
              {element.content || ''}
            </p>
          )}
        </CardContent>
      </Card>
    );
  }

  // ============ BADGE ============
  if (element.type === 'badge') {
    return (
      <Badge
        style={{
          position: 'absolute',
          left: element.x,
          top: element.y,
          backgroundColor: getColor(element.background),
          color: getColor(element.color),
          fontSize: element.fontSize || 12,
          padding: `${getSpacing(element.padding || 4)}px ${getSpacing(element.padding || 8)}px`,
        }}
      >
        {element.content || element.label || 'Badge'}
      </Badge>
    );
  }

  // ============ ALERT ============
  if (element.type === 'alert') {
    return (
      <Alert
        style={{
          position: 'absolute',
          left: element.x,
          top: element.y,
          width: element.width,
          height: element.height,
          backgroundColor: getColor(element.background),
          borderColor: getColor(element.borderColor),
          borderRadius: element.borderRadius || 6,
        }}
      >
        <AlertCircle className="h-4 w-4" />
        <AlertTitle style={{ color: getColor(element.titleColor) }}>
          {element.title || 'Alert'}
        </AlertTitle>
        <AlertDescription style={{ color: getColor(element.color) }}>
          {element.content || element.description || ''}
        </AlertDescription>
      </Alert>
    );
  }

  // ============ CONTAINER / SECTION / HEADER / BOTTOM_NAV ============
  if (element.type === 'container' || element.type === 'section' || element.type === 'header' || element.type === 'div' || element.type === 'bottom_nav') {
    return (
      <div
        style={{
          position: 'absolute',
          left: element.x || 0,
          top: element.y || 0,
          width: element.width || 'auto',
          height: element.height || 'auto',
          backgroundColor: getColor(element.background),
          padding: getSpacing(element.padding),
          borderRadius: element.borderRadius || 0,
          display: 'flex',
          flexDirection: element.flexDirection === 'row' ? 'row' : 'column',
          gap: getSpacing(element.gap),
          border: element.border ? `1px solid ${getColor(element.border)}` : 'none',
          borderTop: element.borderTop || 'none',
        }}
      >
        {element.elements && element.elements.length > 0 ? (
          <div style={{ position: 'relative', width: '100%', height: '100%' }}>
            {element.elements.map((child: any, idx: number) => (
              <DynamicComponent
                key={`${element.id}-${idx}`}
                element={child}
                tokens={tokens}
              />
            ))}
          </div>
        ) : element.children && element.children.length > 0 ? (
          element.children.map((child: any, idx: number) => (
            <DynamicComponent
              key={`${element.id}-${idx}`}
              element={child}
              tokens={tokens}
            />
          ))
        ) : element.items ? (
          <div style={{ display: 'flex', justifyContent: 'space-around', width: '100%', alignItems: 'center', height: '100%' }}>
            {element.items.map((item: any, idx: number) => (
              <div key={idx} style={{ textAlign: 'center', fontSize: 12, color: '#666' }}>
                <span style={{ fontSize: 20 }}>{item.icon === 'home' ? '🏠' : item.icon === 'search' ? '🔍' : item.icon === 'profile' ? '👤' : '📱'}</span>
                <div>{item.label}</div>
              </div>
            ))}
          </div>
        ) : (
          <span style={{ color: getColor(element.color) }}>
            {element.content || ''}
          </span>
        )}
      </div>
    );
  }

  // ============ IMAGE ============
  if (element.type === 'image') {
    return (
      <div
        style={{
          position: 'absolute',
          left: element.x,
          top: element.y,
          width: element.width,
          height: element.height,
          backgroundColor: '#f0f0f0',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          color: '#999',
          borderRadius: element.borderRadius || 8,
          border: '1px solid #ddd',
        }}
      >
        📷 {element.alt || 'Image'}
      </div>
    );
  }

  // ============ DEFAULT FALLBACK ============
  return (
    <div
      style={{
        position: 'absolute',
        left: element.x,
        top: element.y,
        width: element.width,
        height: element.height,
        backgroundColor: '#fff3cd',
        padding: 8,
        border: '1px dashed #ff9800',
        borderRadius: 4,
        fontSize: 12,
        color: '#666',
      }}
    >
      <small>Unknown: {element.type}</small>
    </div>
  );
};
