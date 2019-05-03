#ifndef _XI2C_H_
#define _XI2C_H_

#include <stdint.h>

int i2c_open(const char *dev, int id);
int i2c_close(int fd);
int i2c_writereg(int fd, uint8_t reg, uint8_t data);
int i2c_writereg16(int fd, uint8_t reg, uint16_t data);
int i2c_readreg(int fd, uint8_t reg);
int i2c_readreg16(int fd, uint8_t reg);
int i2c_readreg24(int fd, uint8_t reg);
int i2c_writewreg(int fd, uint16_t reg, uint8_t data);
int i2c_writewreg16(int fd, uint16_t reg, uint16_t data);
int i2c_readwreg(int fd, uint16_t reg);
int i2c_readwreg16(int fd, uint16_t reg);

#endif /* _XI2C_H_ */
