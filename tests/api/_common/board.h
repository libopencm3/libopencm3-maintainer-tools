/*
 * This file is part of the libopencm3 project.
 *
 * Copyright (C) 2014 Frantisek Burian <BuFran@seznam.cz>
 *
 * This library is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Lesser General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This library is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public License
 * along with this library.  If not, see <http://www.gnu.org/licenses/>.
 */
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
