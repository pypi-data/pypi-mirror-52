// Copyright 2018 leoetlino <leo@leolam.fr>
// Licensed under GPLv2+

#pragma once

#include <cstring>

#include "swap.h"

#ifndef _WIN32
#include <arpa/inet.h>
#endif

namespace common {

namespace detail {
inline bool isBigEndianPlatform() {
#ifdef _WIN32
  return false;
#else
  return htonl(0x12345678) == 0x12345678;
#endif
}

template <typename T>
T swapIfNeeded(T value, bool bigEndian) {
  if (isBigEndianPlatform() != bigEndian)
    value = SwapValue(value);
  return value;
}
}  // namespace detail

/// A simple binary data reader that automatically byteswaps and avoids undefined behaviour.
class BinaryReader final {
public:
  BinaryReader(const u8* data, bool bigEndian) : mData{data}, mBigEndian{bigEndian} {}

  bool isBigEndian() const { return mBigEndian; }
  const u8* data() const { return mData; }

  template <typename T>
  T read(size_t offset) const {
    T value;
    std::memcpy(&value, &mData[offset], sizeof(T));
    return detail::swapIfNeeded(value, mBigEndian);
  }

  u32 readU24(size_t offset) const {
    if (mBigEndian)
      return mData[offset] << 16 | mData[offset + 1] << 8 | mData[offset + 2];
    return mData[offset + 2] << 16 | mData[offset + 1] << 8 | mData[offset];
  }

  const char* getString(size_t offset) const {
    return reinterpret_cast<const char*>(&mData[offset]);
  }

private:
  const u8* mData = nullptr;
  bool mBigEndian = false;
};

}  // namespace common
