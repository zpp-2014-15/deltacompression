#include "chunker.h"
#include "cool/types.h"
#include <memory>
#include <fstream>
#include <streambuf>
#include <string>
#include <algorithm>
#include <iostream>

size_t getChunkSize(const cool::IoVec &chunk) {
    return chunk[0].iov_len;
}

int processFile(const std::string &fileName, hydra::chunking::ChunkerAdapter &adapter) {
    std::ifstream in(fileName, std::ios::binary | std::ios::in);
    if (!in) {
        throw "Couldn't open file " + fileName + ".";
    }
    in.exceptions(std::ifstream::failbit | std::ifstream::badbit);
    in.seekg(0, std::ios::end);

    size_t content_size = in.tellg();
    if (content_size != 0) {
        std::unique_ptr<char[]> content(new char[content_size]);

        in.seekg(0, std::ios::beg);

        std::copy(std::istreambuf_iterator<char>(in),
                  std::istreambuf_iterator<char>(),
                  content.get());
        in.close();
        cool::IoVec data;
        data.push_back(content.get(), content_size);
        adapter.add(data);

        // we'll be only writing sizes of consecutive chunks to output
        while (adapter.haveChunk()) {
            std::cout << getChunkSize(adapter.getChunkRef()) << std::endl;
        }

        while (!adapter.isEmpty()) {
            std::cout << getChunkSize(adapter.getTerminalChunkRef()) << std::endl;
        }
    }

    std::cout << -1 << std::endl;
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

    hydra::chunking::ChunkerAdapter adapter(minChunk, maxChunk, avgChunk);
    std::string fileName;

    try {
        while (std::getline(std::cin, fileName)) {
            processFile(fileName, adapter);
        }
    }
    catch(const char *e) {
        std::cerr << *e << std::endl;
        return EXIT_FAILURE;
    }

    return 0;
}
