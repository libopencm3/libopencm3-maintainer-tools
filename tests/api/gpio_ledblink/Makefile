BINARY		= ledblink
OPENCM3_DIR	= ../../../libopencm3
CPPFLAGS		+= -DBOARD=$(BOARD)

ifeq ($(BOARD),stm32f0discovery)
LIBNAME		= opencm3_stm32f0
DEFS		= -DSTM32F0

FP_FLAGS	?= -msoft-float
ARCH_FLAGS	= -mthumb -mcpu=cortex-m0 $(FP_FLAGS)
endif

include ../../../Makefile.rules