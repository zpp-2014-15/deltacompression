#include "chunker.h"
#include "cool/types.h"
#include <memory>
#include <cassert>
#include <list>
#include <utility>
#include <fstream>
#include <streambuf>
#include <string>
#include <algorithm>
#include <iostream>


class ChunkerAdapter {
private:
    std::list<std::pair<std::shared_ptr<char>, size_t>> regions;
    hydra::chunking::ChunkerAdapter adapter;
    void removeChunk(size_t ch_size) {
        while (ch_size) {
            auto && region = regions.front();
            if (region.second > ch_size) {
                region.second -= ch_size;
                ch_size = 0;
            }
            else {
                ch_size -= region.second;
                regions.pop_front();
            }
        }
    }

public:
    ChunkerAdapter(int minChunk, int maxChunk, int avgChunk)
        : adapter(minChunk, maxChunk, avgChunk) {}

    void addMemoryRegion(const std::shared_ptr<char> &cont, size_t size) {
        cool::IoVec data;
        data.push_back(cont.get(), size);
        adapter.add(data);
        regions.push_back(std::make_pair(cont, size));
    }

    bool haveChunk() { return adapter.haveChunk(); }
    bool isEmpty() { return adapter.isEmpty(); }
    size_t getChunk() {
        assert(haveChunk());
        size_t bytes = adapter.getChunkRef().getTotalBytes();
        removeChunk(bytes);
        return bytes;
    }

    size_t getTerminalChunk() {
        assert(!isEmpty());
        size_t bytes = adapter.getTerminalChunkRef().getTotalBytes();
        removeChunk(bytes);
        return bytes;
    }
};


int processFile(const std::string &fileName, ChunkerAdapter &adapter) {
    std::ifstream in(fileName, std::ios::binary | std::ios::in);
    if (!in) {
        throw "Failed to open the file.";
    }
    in.exceptions(std::ifstream::failbit | std::ifstream::badbit);
    in.seekg(0, std::ios::end);

    std::cout << -1 << std::endl;

    size_t content_size = in.tellg();
    if (content_size != 0) {
        std::shared_ptr<char> content(new char[content_size]);

        in.seekg(0, std::ios::beg);

        std::copy(std::istreambuf_iterator<char>(in),
                  std::istreambuf_iterator<char>(),
                  content.get());
        in.close();

        adapter.addMemoryRegion(content, content_size);
        // we'll be only writing sizes of consecutive chunks to output
        while (adapter.haveChunk())
            std::cout << adapter.getChunk() << std::endl;
    }

    return 0;
}

int main(int argc, char* argv[]) {
    if (argc < 4) {
        std::cerr << "Usage " << argv[0]
                  << " minchunk maxchunk avgchunk" << std::endl;
        return EXIT_FAILURE;
    }

    int minChunk = std::stoi(std::string(argv[1]));
    int maxChunk = std::stoi(std::string(argv[2]));
    int avgChunk = std::stoi(std::string(argv[3]));

    ChunkerAdapter adapter(minChunk, maxChunk, avgChunk);
    std::string fileName;

    while (std::getline(std::cin, fileName)) {
        try {
            processFile(fileName, adapter);
        }
        catch(const char *e) {
            std::cerr << "Error when processing file " << fileName << ": "
                      << e << std::endl;
            return EXIT_FAILURE;
        }
    }

    while (!adapter.isEmpty())
        std::cout << adapter.getTerminalChunk() << std::endl;

    return 0;
}
