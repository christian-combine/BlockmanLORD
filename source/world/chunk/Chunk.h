/********************************************************************
author: Comical
company: Spargat
*********************************************************************/
#ifndef CHUNK_H_GUARD
#define CHUNK_H_GUARD

#include <cstdint>
#include <utility>

#include "../../tile/Block.h"

class BlockInfo;
class BlockAddress;
class BlockState;

class ChunkSection;

class NBT_Tag_Compound;
class NBT_Tag_Byte_Array;
class NBT_File;

class Chunk
{
	public:
		typedef std::pair<int32_t, int32_t> Key;
		
		static const int32_t MAX_SECTIONS = 16;
		
		Chunk(int t, int x, int z, int co, int cl);
		~Chunk();
		
		bool load(NBT_File *fh);
		bool save(NBT_File *buff);
		
		int32_t x() { return x_pos; }
		int32_t z() { return z_pos; }
		
		void setTimestamp(uint32_t timestamp) { this->timestamp = timestamp; }
		int getTimestamp() { return timestamp; }
		
		uint32_t offset() { return chunk_offset; }
		uint32_t len() { return chunk_len; }

      NBT_Tag_Compound *nbt() { return nbt_data; }
      
      const Key key() const { return Key(x_pos, z_pos); }
      static const Key key(int32_t x, int32_t z) { return Key(x, z); }
      
      bool getBlockAddress(int32_t x, int32_t y, int32_t z, BlockAddress *addr);
      bool getBlockInfo(const BlockAddress &addr, BlockInfo *info);
      
		uint32_t sectionCount();
		ChunkSection *getSection(uint32_t idx);
		
	private:
		int32_t x_pos;
		int32_t z_pos;
		uint32_t timestamp;
		
		uint32_t chunk_offset;
		uint32_t chunk_len;
		
      NBT_Tag_Compound *nbt_data;
		NBT_Tag_Byte_Array *biome_data;
		
		uint32_t m_section_count;
		ChunkSection *sections[MAX_SECTIONS];
};

#endif /* CHUNK_H_GUARD */
