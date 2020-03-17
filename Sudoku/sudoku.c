#include <stdio.h>
#include <stdlib.h>

#define N 9

// example board and input format
char *board = "4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......";

// print board in a box using '-' and '|' ASCII characters
void print_board(int board[N][N]) {
    char *Line = "\n  -----------------------\n";
    printf("%s", Line);

    for (int i = 0; i < N; i++) {
        for(int j = 0; j < N; j++) {
            if (j%3 == 0) 
                printf(" |");
            printf("%2d", board[i][j]);
        }

        printf(" |");

        if ((i+1) %3 == 0)
            printf("%s", Line);
        else
            printf("\n");
    }
    printf("\n");
}

// function to find the next empty position on the board
int find_empty_cell(int board[N][N], int* r, int* c) {
    for (*r = 0; *r < N; (*r)++)
        for (*c = 0; *c < N; (*c)++)
            if (board[*r][*c] == 0)
                return 0;
    return 1;
}

// check if the value n satisfies the rules for board position at (r, c)
int check_valid_pos(int board[N][N], int r, int c, int n) {
    // check if column contains duplicate value
    for (int i = 0; i < N; i++)
        if (board[r][i] == n)
            return 0;

    // check if row contains duplicate value
    for (int i = 0; i < N; i++)
        if (board[i][c] == n)
            return 0;

    // find the grid which contains (r, c)
    r -= (r % 3);
    c -= (c % 3);

    // check if 3x3 grid contains duplicate value
    for (int i = 0; i < 3; i++)
        for (int j = 0; j < 3; j++)
            if (board[i + r][j + c] == n)
                return 0;
    return 1;
}

int solve(int board[N][N]) {
    int  r = 0;
    int  c = 0;

    // find next empty cell on board and if no cell is found board is solved
    if(find_empty_cell(board, &r, &c))
        return 1;

    for (int i = 1; i <= N; i++) {
        // check all values from 1..N as candidate for empty cell
        if(check_valid_pos(board, r, c, i)) {
            // fill valid value i at board pos (r, c)
            board[r][c] = i;

            // recurse with empty cell filled and if board is solved return
            if (solve(board))
                return 1;

            // backtrack with reseting board pos (r, c)
            board[r][c] = 0;
        }
    }
    // no solution found for given board configuration
    return 0;
}

void parse_line(char *line) {
    // create 9x9 2d array with initial value 0
    int board[N][N] = {0};

    // fill the 2d array with value from board string
    for(int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            if(line[i * N + j] != '.') {
                char ch = line[i*N +j];
                board[i][j] = atoi(&ch);
            }
        }
    }

    //print parsed board
    print_board(board);

    // check if board is solvable and print solved board
    if(solve(board))
        print_board(board);
    else
        printf("No solution \n");
}


int main() {
    printf("Input board: %s\n", board);
    printf("Solved board:");
    parse_line(board);
    return 0;
}
