'use client';

import React, { useState } from 'react';
import { DynamicComponent } from './DynamicComponent';

interface Screen {
  id: string;
  name: string;
  type?: 'mobile' | 'tablet' | 'web';
  width: number;
  height: number;
  background: string;
  elements: any[];
}

interface DesignData {
  screens: Screen[];
  design_tokens?: any;
}

interface DesignCanvasProps {
  design: DesignData | null;
  loading?: boolean;
}

/**
 * DESIGN CANVAS RENDERER
 * Renders ANY design from LLM response
 * 100% data-driven, NO hardcoding
 */
export const DesignCanvas: React.FC<DesignCanvasProps> = ({ design, loading = false }) => {
  const [selectedScreen, setSelectedScreen] = useState(0);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
          <p className="mt-4 text-gray-600">Generating design...</p>
        </div>
      </div>
    );
  }

  if (!design || !design.screens || design.screens.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center h-96 text-gray-500">
        <p className="text-2xl mb-2">✨ No design yet</p>
        <p className="text-sm">Create a design request to see it rendered here</p>
      </div>
    );
  }

  const currentScreen = design.screens[selectedScreen];

  return (
    <div className="w-full bg-gradient-to-b from-gray-50 to-gray-100 rounded-lg p-6">
      {/* Screen Tabs */}
      {design.screens.length > 1 && (
        <div className="mb-6 border-b border-gray-200 flex gap-2 overflow-x-auto pb-2">
          {design.screens.map((screen, idx) => (
            <button
              key={screen.id}
              onClick={() => setSelectedScreen(idx)}
              className={`px-4 py-2 rounded-t-lg font-medium transition ${
                selectedScreen === idx
                  ? 'bg-blue-500 text-white'
                  : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
              }`}
            >
              {screen.name || `Screen ${idx + 1}`}
            </button>
          ))}
        </div>
      )}

      {/* Screen Info */}
      <div className="mb-4 flex justify-between items-center">
        <h3 className="text-lg font-semibold text-gray-900">
          {currentScreen.name || 'Screen'}
        </h3>
        <span className="text-sm text-gray-600 font-mono">
          {currentScreen.width}×{currentScreen.height} ({currentScreen.type || 'mobile'})
        </span>
      </div>

      {/* Canvas Frame */}
      <div className="flex justify-center">
        <div
          className="relative bg-white border-2 border-gray-300 shadow-lg rounded-lg overflow-hidden"
          style={{
            width: currentScreen.width,
            height: currentScreen.height,
            backgroundColor: currentScreen.background || '#ffffff',
          }}
        >
          {currentScreen.elements && currentScreen.elements.length > 0 ? (
            currentScreen.elements.map((element, idx) => (
              <DynamicComponent
                key={`${element.id || idx}`}
                element={element}
                tokens={design.design_tokens}
              />
            ))
          ) : (
            <div className="flex items-center justify-center h-full text-gray-400">
              <p>No elements in this screen</p>
            </div>
          )}
        </div>
      </div>

      {/* Design Tokens Info */}
      {design.design_tokens && (
        <div className="mt-6 bg-white rounded-lg border border-gray-200 p-4">
          <details className="cursor-pointer">
            <summary className="font-semibold text-gray-900 mb-2">
              📋 Design System
            </summary>
            <pre className="bg-gray-50 p-3 rounded text-xs overflow-x-auto text-gray-700">
              {JSON.stringify(design.design_tokens, null, 2)}
            </pre>
          </details>
        </div>
      )}
    </div>
  );
};
