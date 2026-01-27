export enum Direction {
  UP = 'UP',
  DOWN = 'DOWN',
  LEFT = 'LEFT',
  RIGHT = 'RIGHT',
  NONE = 'NONE'
}

export interface LogEntry {
  id: string;
  timestamp: string;
  message: string;
  type: 'info' | 'warning' | 'error' | 'success';
}

export interface ControlState {
  direction: Direction;
  buttons: {
    a: boolean;
    b: boolean;
    x: boolean;
    y: boolean;
  };
}