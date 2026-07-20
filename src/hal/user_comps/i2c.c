#include <err.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/ioctl.h>
#include <unistd.h>

#include "i2c.h"

#define I2C_SLAVE 0x0703
#define I2C_SMBUS 0x0720

int i2c_open(const char *dev, int id) {
  int fd;

  if ((fd = open(dev, O_RDWR)) < 0)
    errx(1, "i2c device [%s] open failed", dev);

  if (ioctl(fd, I2C_SLAVE, id) < 0)
    errx(1, "i2c device addr ioctl failed");

  return fd;
}

int i2c_close(int fd) { return close(fd); }

int i2c_writereg(int fd, uint8_t reg, uint8_t data) {
  char buf[] = {reg, data};

  if (write(fd, buf, sizeof(buf)) != sizeof(buf))
    return -1;
  return 0;
}

int i2c_writereg16(int fd, uint8_t reg, uint16_t data) {
  char buf[] = {reg, (data >> 8) & 0xff, data & 0xff};

  if (write(fd, buf, sizeof(buf)) != sizeof(buf))
    return -1;
  return 0;
}

int i2c_readreg(int fd, uint8_t reg) {
  char buf[] = {reg};
  uint8_t val[1];

  if (write(fd, buf, sizeof(buf)) != sizeof(buf))
    return -1;
  if (read(fd, val, sizeof(val)) != sizeof(val))
    return -1;
  return val[0];
}

int i2c_readreg16(int fd, uint8_t reg) {
  char buf[] = {reg};
  uint8_t val[2];

  if (write(fd, buf, sizeof(buf)) != sizeof(buf))
    return -1;
  if (read(fd, val, sizeof(val)) != sizeof(val))
    return -1;
  return (val[0] << 8) | val[1];
}

int i2c_readreg24(int fd, uint8_t reg) {
  char buf[] = {reg};
  uint8_t val[3];

  if (write(fd, buf, sizeof(buf)) != sizeof(buf))
    return -1;
  if (read(fd, val, sizeof(val)) != sizeof(val))
    return -1;
  return (val[0] << 16) | (val[1] << 8) | val[2];
}

int i2c_writewreg(int fd, uint16_t reg, uint8_t data) {
  char buf[] = {(reg >> 8) & 0xff, reg & 0xff, data};

  if (write(fd, buf, sizeof(buf)) != sizeof(buf))
    return -1;
  return 0;
}

int i2c_writewreg16(int fd, uint16_t reg, uint16_t data) {
  char buf[] = {(reg >> 8) & 0xff, reg & 0xff, (data >> 8) & 0xff, data & 0xff};

  if (write(fd, buf, sizeof(buf)) != sizeof(buf))
    return -1;
  return 0;
}

int i2c_readwreg(int fd, uint16_t reg) {
  char buf[] = {(reg >> 8) & 0xff, reg & 0xff};
  uint8_t val[1];

  if (write(fd, buf, sizeof(buf)) != sizeof(buf))
    return -1;
  if (read(fd, val, sizeof(val)) != sizeof(val))
    return -1;
  return val[0];
}

int i2c_readwreg16(int fd, uint16_t reg) {
  char buf[] = {(reg >> 8) & 0xff, reg & 0xff};
  uint8_t val[2];

  if (write(fd, buf, sizeof(buf)) != sizeof(buf))
    return -1;
  if (read(fd, val, sizeof(val)) != sizeof(val))
    return -1;
  return (val[0] << 8) | val[1];
}
