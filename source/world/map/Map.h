/********************************************************************
author: Comical
company: Spargat
*********************************************************************/
#ifndef MAP_H_GUARD
#define MAP_H_GUARD

#include <vector>
#include <string>
#include <unordered_map>
#include "MCRegion.h"

class NBT;

class Map
{	
	public:
		typedef std::unordered_map<typename MCRegion::Key, MCRegion *> RegionMap;
		
		Map(const std::string &path);
		~Map();
		
		bool load();
		bool save();
		bool saveTo(const std::string &path);
		
		MCRegion *firstRegion();
		MCRegion *nextRegion();
		
		int numRegions() { return data.size(); }
		
		MCRegion *getRegion(int32_t x, int32_t z);
		MCRegion *getRegionForChunk(int32_t x, int32_t z);
		
		Chunk *getChunk(int32_t x, int32_t z);
		
		std::string mapPath() const { return map_path; }
		std::string mapName() const { return map_name; }
		
		int32_t dimension() { return dimension_id; }
		
	private:
		const std::string map_path;
		std::string map_name;
		int32_t dimension_id;
		
		RegionMap::iterator dataIterator_;
		RegionMap data;
};

#endif /* MAP_H_GUARD */
