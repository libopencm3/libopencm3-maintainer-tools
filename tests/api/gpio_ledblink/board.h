#ifndef __BOARD_H__
#define __BOARD_H__

#if !defined(BOARD)
# error Preprocessor directive 'BOARD' not specified. Stop.
#endif

struct pin_config
{
	uint32_t port;
	uint32_t pin;
	uint32_t clock;
};

/******************************************************************************
 * Board-specific file inclusion "board/${BOARD}.h" file)
 ******************************************************************************/

#define __QUOTE(m)		#m
#define __FN(a,b,c)		__QUOTE(a/b.c)
#define __BOARD_H_FILE(brd)	__FN(boards,brd,h)

#include __BOARD_H_FILE(BOARD)

#endif /* __BOARD_H__ */
