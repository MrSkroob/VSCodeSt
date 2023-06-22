#include <time.h>
#include <stdlib.h>

// NOTE: SCREEN SIZE IS 320x240
#define SCREEN_WIDTH 320
#define SCREEN_HEIGHT 240

// BLOCK CONSTANTS
#define MATRIX_SIZE 16
#define SMALL_MATRIX_SIZE = 9
#define MATRIX_WIDTH 4
#define SMALL_MATRIX_WIDTH = 3
#define BLOCK_WIDTH 10

#define BOARD_WIDTH 110
#define BOARD_HEIGHT 160
#define BOARD_BLOCK_WIDTH BOARD_WIDTH / 10
#define BOARD_BLOCK_HEIGHT BOARD_HEIGHT / 10
#define BOARD_X (SCREEN_WIDTH - BOARD_WIDTH) / 2
#define BOARD_Y (SCREEN_HEIGHT - BOARD_HEIGHT) / 2
#define NUMBER_OF_BLOCKS BOARD_BLOCK_WIDTH * BOARD_BLOCK_HEIGHT


// block definitions
int const I_BLOCK[MATRIX_SIZE] = {
  0, 0, 0, 0,
  1, 1, 1, 1,
  0, 0, 0, 0,
  0, 0, 0, 0,
};
int const L_BLOCK_LEFT[SMALL_MATRIX_SIZE] = {
  1, 0, 0,
  1, 1, 1,
  0, 0, 0
};
int const L_BLOCK_RIGHT[SMALL_MATRIX_SIZE] = {
  0, 0, 1,
  1, 1, 1,
  0, 0, 0
};
int const O_BLOCK[MATRIX_SIZE] = {
  0, 0, 0, 0,
  0, 1, 1, 0,
  0, 1, 1, 0,
  0, 0, 0, 0
};
int const S_BLOCK_LEFT[SMALL_MATRIX_SIZE] = {
  0, 1, 1,
  1, 1, 0,
  0, 0, 0
};
int const S_BLOCK_RIGHT[SMALL_MATRIX_SIZE] = {
  1, 1, 0,
  0, 1, 1,
  0, 0, 0
};
int const T_BLOCK[SMALL_MATRIX_SIZE] = {
  0, 1, 0,
  1, 1, 1,
  0, 0, 0
};
typedef struct Shapes {
  int block[16];
  int x;
  int y;
  int matrix_width;
  int matrix_size;
  Channel sprite;
} Shape;


void apply_changes(const int* new_array, int* block_array, int array_sizes) { // copies the new_array to 
  for (int i = 0; i < array_sizes; i++) {                               // the block array
    block_array[i] = new_array[i];
  }
}


void reverse_rows(int* block_array, int matrix_size, int matrix_width) { // reverses the rows in a 4x4 (16) id array
  int copy[matrix_size];
  for (int i = 0; i < matrix_width; i++) {
    for (int j = matrix_width; j > 0; j--) {
      int index = i * matrix_width - 1 + j; // j = collumn, i = row
      int reversed_index = i * matrix_width + (matrix_width - j);
      copy[reversed_index] = block_array[index];
    }
  }
  apply_changes(copy, block_array, MATRIX_SIZE);
}


void reverse_collumns(int* block_array, int matrix_size, int matrix_width) { // reverses the collumns in a 4x4 (16) 1d array
  int copy[matrix_size];
  for (int i = 0; i < matrix_width; i++) {
    int collumn_copy[matrix_width];
    for (int j = 0; j < matrix_width; j++) {
      int index = j * matrix_width + i;
      collumn_copy[j] = block_array[index];
    }
    for (int j = 0; j < matrix_width; j++) {
      int index = j * matrix_width + i;
      copy[index] = collumn_copy[matrix_width - 1 - j];
    };
  }
  apply_changes(copy, block_array, matrix_size);
}


void transpose(int* block_array, int matrix_size, int matrix_width) { // transposes the 4x4 (16) 1d array
  int copy[matrix_size];
  for (int i = 0; i < matrix_width; i++) {
    for (int j = 0; j < matrix_width; j++) {
      int index = i * matrix_width + j;
      int swapped_index = i + j * matrix_width;
      int temp = block_array[index];
      copy[swapped_index] = temp;
    }
  };
  apply_changes(copy, block_array, matrix_size);
};


void print_array(int* array, int matrix_width) { // helper function to print out an array
  PutText(Trace, "\n");
  for (int i = 0; i < matrix_width; i++) {
    for (int j = 0; j < matrix_width; j++) {
      int index = i * matrix_width + j;
      PutInt64AsText(Trace, array[index]);
    }
    PutText(Trace, "\n");
  }
}


void rotate_90_CW(Shape* shape) {
  // rotates the tetris piece 90 degrees clockwise
  int matrix_size = shape.matrix_size
  int matrix_width = shape.matrix_width
  transpose(block_array, matrix_size, matrix_width);
  reverse_collumns(block_array, matrix_size, matrix_width);
};


void rotate_90_CCW(Shape* shape) { //replaced int* block_array, int matrix_size, int matrix_width
  // rotates the tetris piece 90 degrees counter clockwise
  int matrix_size = shape.matrix_size
  int matrix_width = shape.matrix_width
  reverse_rows(shape.block_array, matrix_size, matrix_width);
  transpose(shape.block_array, matrix_size, matrix_width);
}


int get_random(int lower, int upper) {
  // returns a random integer between the lower and upper bounds, inclusive
  return (rand() % (upper - lower + 1) + (lower - 1));
}


void draw(Channel io, Channel sprite, int x, int y) {
  BeginDraw(io);
  DrawSprite(io, sprite, x, y);
  EndDraw(io);
}


void draw_shape(Channel io, Shape shape, Channel sprite) {
  BeginDraw(io);
  int matrix_width = shape.matrix_width
  for (int i = 0; i < matrix_width; i += 1) {
    for (int j = 0; j < matrix_width; j += 1) {
      int index = i * matrix_width + j;
      if (shape.block[index] == 1) {
	DrawSprite(io, sprite, shape.x + i * BLOCK_WIDTH, shape.y + j * BLOCK_WIDTH);
      };
    }
  }
  EndDraw(io);
}


void draw_space(Channel io, Channel sprite, int x1, int y1, int x2, int y2) {
  BeginDraw(io);
  for (int i = x1; i < x2; i += BLOCK_WIDTH) {
    for (int j = y1; j < y2; j += BLOCK_WIDTH) {
      DrawSprite(io, sprite, i, j);
    }
  }
  EndDraw(io);
}


void Main(Channel io) {
  Channel cyan_block = LoadNewSprite("sprite", io, "cyan_block");
  Channel red_block = LoadNewSprite("sprite", io, "red_block");
  Channel blue_block = LoadNewSprite("sprite", io, "blue_block");
  Channel green_block = LoadNewSprite("sprite", io, "green_block");
  Channel orange_block = LoadNewSprite("sprite", io, "orange_block");
  Channel yellow_block = LoadNewSprite("sprite", io, "yellow_block");
  Channel black_block = LoadNewSprite("sprite", io, "black_block");

  srand(time(NULL));

  int board[NUMBER_OF_BLOCKS];

  int i_block[MATRIX_SIZE];
  int l_block_left[SMALL_MATRIX_SIZE];
  int l_block_right[SMALL_MATRIX_SIZE];
  int o_block[MATRIX_SIZE];
  int s_block_left[SMALL_MATRIX_SIZE];
  int s_block_right[SMALL_MATRIX_SIZE];
  int t_block[SMALL_MATRIX_SIZE];

  apply_changes(I_BLOCK, i_block, MATRIX_SIZE); // copy the array to tetris_piece
  apply_changes(L_BLOCK_LEFT, l_block_left, SMALL_MATRIX_SIZE);
  apply_changes(L_BLOCK_RIGHT, l_block_right, SMALL_MATRIX_SIZE);
  apply_changes(O_BLOCK, o_block, MATRIX_SIZE);
  apply_changes(S_BLOCK_LEFT, s_block_left, SMALL_MATRIX_SIZE);
  apply_changes(S_BLOCK_RIGHT, s_block_right, SMALL_MATRIX_SIZE);
  apply_changes(T_BLOCK, t_block, SMALL_MATRIX_SIZE);
  
  Shape i_shape;
  i_shape.sprite = cyan_block;
  i_shape.matrix_size = MATRIX_SIZE
  i_shape.matrix_width = MATRIX_WIDTH
  apply_changes(i_block, i_shape.block, MATRIX_SIZE);

  Shape l_shape_left;
  l_shape_left.sprite = red_block;
  l_shape_left.matrix_size = SMALL_MATRIX_SIZE
  l_shape_left.matrix_width = SMALL_MATRIX_WIDTH
  apply_changes(l_block_left, l_shape_left.block, SMALL_MATRIX_SIZE);
  
  Shape l_shape_right;
  l_shape_right.sprite = blue_block;
  l_shape_right.matrix_size = SMALL_MATRIX_SIZE
  l_shape_right.matrix_width = SMALL_MATRIX_WIDTH
  apply_changes(l_block_right, l_shape_right.block, SMALL_MATRIX_SIZE);
  
  Shape o_shape;
  o_shape.sprite = green_block;
  o_shape.matrix_size = MATRIX_SIZE
  o_shape.matrix_width = MATRIX_WIDTH
  apply_changes(o_block, o_shape.block, MATRIX_SIZE);
  
  Shape s_shape_left;
  s_shape_left.sprite = green_block;
  s_shape_left.matrix_size = SMALL_MATRIX_SIZE
  s_shape_left.matrix_width = SMALL_MATRIX_WIDTH
  apply_changes(s_block_left, s_shape_left.block, SMALL_MATRIX_SIZE);
  
  Shape s_shape_right;
  s_shape_right.sprite = orange_block;
  s_shape_right.matrix_size = SMALL_MATRIX_SIZE
  s_shape_right.matrix_width = SMALL_MATRIX_WIDTH
  apply_changes(s_block_right, s_shape_right.block, SMALL_MATRIX_SIZE);

  Shape t_shape;
  t_shape.sprite = yellow_block;
  t_shape.matrix_size = SMALL_MATRIX_SIZE
  t_shape.matrix_width = SMALL_MATRIX_WIDTH
  apply_changes(t_block, t_shape.block, SMALL_MATRIX_SIZE);


  Shape current_piece = t_shape;

  current_piece.x = BOARD_X;
  current_piece.y = BOARD_Y;
  
  
  draw_space(io, black_block, BOARD_X, BOARD_Y, BOARD_X + BOARD_WIDTH, BOARD_Y + BOARD_HEIGHT);
  while (True) {
    draw_shape(io, current_piece, black_block);
    rotate_90_CCW(current_piece);
    draw_shape(io, current_piece, current_piece.sprite);
    WaitForKeyPress(io);
  };
}


