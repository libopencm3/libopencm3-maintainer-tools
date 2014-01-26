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
#ifndef __STM32F3DISCOVERY_H__
#define __STM32F3DISCOVERY_H__

#define BOARD_NAME		"STM32F3-Discovery"

/******************************************************************************
 * LED configuration
 ******************************************************************************/

struct pin_config board_leds[] = {
	{	/* LD4 Blue */
		.port = GPIOE,
		.pin = GPIO8,
		.clock = RCC_GPIOE,
	} , {	/* LD6 Green */
		.port = GPIOE,
		.pin = GPIO15,
		.clock = RCC_GPIOE,
	} , {	/* LD5 Orange */
		.port = GPIOE,
		.pin = GPIO10,
		.clock = RCC_GPIOE,
	} , {	/* LD3 Red */
		.port = GPIOE,
		.pin = GPIO9,
		.clock = RCC_GPIOE,
	} , {	/* LD7 Green */
		.port = GPIOE,
		.pin = GPIO11,
		.clock = RCC_GPIOE,
	} , {	/* LD8 Orange */
		.port = GPIOE,
		.pin = GPIO14,
		.clock = RCC_GPIOE,
	} , {	/* LD9 Blue */
		.port = GPIOE,
		.pin = GPIO12,
		.clock = RCC_GPIOE,
	} , {	/* LD10 Red */
		.port = GPIOE,
		.pin = GPIO13,
		.clock = RCC_GPIOE,
	}
};

#define BOARD_NLEDS	sizeof(board_leds) / sizeof(struct pin_config)

#define BOARD_LED_GREEN		1
#define BOARD_LED_BLUE		0
#define BOARD_LED_ORANGE	2
#define BOARD_LED_RED		3

/******************************************************************************
 * BUTTON configuration
 ******************************************************************************/

struct pin_config board_btns[] = {
	{	/* USER KEY */
		.port = GPIOA,
		.pin = GPIO0,
		.clock = RCC_GPIOA,
	}
};

#define BOARD_NBTNS	sizeof(board_btns) / sizeof(struct pin_config)

/******************************************************************************
 * Serial port configuration
 ******************************************************************************/


#endif /* __STM32F0DISCOVERY_H__ */