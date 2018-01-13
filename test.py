import json
import pydesignengine as de

data = '{"nodes":{"node-2363":{"metadata.general.name":"B+TREE NODE","external.links.prev":"False","external.links.next":"False","inter-block.fanout.type":"fixed","inter-block.fanout.fixedValue":20,"inter-block.fanout.function":"","inter-block.partitioning.type":"none","inter-block.partitioning.function":"","inter-block.partitioning.logStructured.filtersPerLevel":"False","inter-block.partitioning.logStructured.filtersPerRun":"False","inter-block.partitioning.logStructured.initialRunSize":0,"inter-block.partitioning.logStructured.maxRunsPerLevel":0,"inter-block.partitioning.logStructured.mergeFactor":0,"inter-block.orderMaintenance.type":"push&insert","inter-block.blockAccess.direct":"True","inter-block.blockAccess.headLink":"False","inter-block.blockAccess.tailLink":"False","intra-block.links.prev":"False","intra-block.links.next":"False","intra-block.links.skipLinks.type":"none","intra-block.links.skipLinks.probability":0,"intra-block.filters.zoneMaps.max":"False","intra-block.filters.zoneMaps.min":"True","intra-block.filters.bloomFilter.active":"False","intra-block.filters.bloomFilter.hashFunctionsNumber":0,"intra-block.filters.bloomFilter.numberOfBits":0,"intra-block.dataRetention.keyRetention.type":"none","intra-block.dataRetention.keyRetention.compression":"","intra-block.dataRetention.keyRetention.function":"","intra-block.dataRetention.valueRetention.type":"none","intra-block.dataRetention.valueRetention.compression":"","intra-block.dataRetention.valueRetention.function":"","intra-block.capacity.type":"balanced","intra-block.capacity.value":0,"intra-block.capacity.function":"","intra-block.utilization.constraint":"none","intra-block.utilization.function":"","intra-block.links.linksMemoryLayout":"scatter","intra-block.filters.filtersMemoryLayout":"scatter","intra-block.dataRetention.retainedDataLayout":"dump","intra-block.blockProperties.storage":"pointed"},"node-6081":{"metadata.general.name":"DATAPAGE (SORTED)","external.links.prev":"False","external.links.next":"True","inter-block.fanout.type":"fixed","inter-block.fanout.fixedValue":256,"inter-block.fanout.function":"","inter-block.partitioning.type":"none","inter-block.partitioning.function":"","inter-block.partitioning.logStructured.filtersPerLevel":"False","inter-block.partitioning.logStructured.filtersPerRun":"False","inter-block.partitioning.logStructured.initialRunSize":0,"inter-block.partitioning.logStructured.maxRunsPerLevel":0,"inter-block.partitioning.logStructured.mergeFactor":0,"inter-block.orderMaintenance.type":"push&insert","inter-block.blockAccess.direct":"True","inter-block.blockAccess.headLink":"False","inter-block.blockAccess.tailLink":"False","intra-block.links.prev":"False","intra-block.links.next":"False","intra-block.links.skipLinks.type":"none","intra-block.links.skipLinks.probability":0,"intra-block.filters.zoneMaps.max":"False","intra-block.filters.zoneMaps.min":"False","intra-block.filters.bloomFilter.active":"False","intra-block.filters.bloomFilter.hashFunctionsNumber":0,"intra-block.filters.bloomFilter.numberOfBits":0,"intra-block.dataRetention.keyRetention.type":"full","intra-block.dataRetention.keyRetention.compression":"uncompressed","intra-block.dataRetention.keyRetention.function":"","intra-block.dataRetention.valueRetention.type":"full","intra-block.dataRetention.valueRetention.compression":"uncompressed","intra-block.dataRetention.valueRetention.function":"","intra-block.capacity.type":"fixed","intra-block.capacity.value":1,"intra-block.capacity.function":"","intra-block.utilization.constraint":"leq_capacity","intra-block.utilization.function":"","intra-block.links.linksMemoryLayout":"scatter","intra-block.filters.filtersMemoryLayout":"scatter","intra-block.dataRetention.retainedDataLayout":"columnar","intra-block.blockProperties.storage":"none"}},"edges":{"0":{"sourceId":"node-2363","targetId":"node-2363","text":"log(nPuts)"},"1":{"sourceId":"node-2363","targetId":"node-6081","text":"label-invisible"}},"workload":{"id":"workload","puts":"500","gets":"500","width":"500","position":{"x":800,"y":600}}}'

# print json.loads(data)

def str2num(s):
    try:
        return int(s)
    except ValueError:
        return s

def simulate():

    setting = json.loads(data)
    nodes = setting["nodes"]
    workload = setting["workload"]
    context = {}

    def refresh():
        print(">>> Generating data...")

        #1. width
        widthValue = int(workload["width"])
        readWriteRatio1 = 0
        readWriteRatio2 = 1

        #2. num of puts
        numPuts = int(workload["puts"])
        dist1 = de.UniformDistribution(913812, 1, widthValue)
        generator1 = de.QueryWorkloadGenerator(0, numPuts, dist1)
        workload1 = generator1.generate()
        queryblock_puts = workload1.getBlock(1)

        #3. num of gets
        numGets = int(workload["gets"])
        dist2 = de.UniformDistribution(913812, 1, widthValue)
        generator2 = de.QueryWorkloadGenerator(1, numGets, dist2);
        workload2 = generator2.generate()
        queryblock_gets = workload2.getBlock(1)

        length = 0
        x = de.SystemDesignOptionHierarchy()
        for name in nodes:
            node = nodes[name]
            for prop in node:
                length += 1
                value = node[prop]
                # print str(prop) + ': ' + str(value)
                node[prop] = str2num(value)
                if(value == "False"):
                    node[prop] = False
                elif(value == "True"):
                    node[prop] = True
            # print length
            node_proper = json.dumps(node)
            arch = de.ArchetypeDefinition()
            arch.fromJson(node_proper)
            opt = de.SystemDesignOption(arch, True)
            x += opt
        ef = de.ElementFactory(x)
        element = ef.generate()
        path = "models.txt".encode('utf-8')
        models = de.MicroBenchmark()
        # models.load(path)
        # print models
        # res = element.estimateGets(queryblock_puts, queryblock_gets, models, None)
        # print res

        # estimateGets(design_engine::data::QueryBlock *puts,
        #              design_engine::data::QueryBlock *gets,
        #              design_engine::micro_benchmarks::MicroBenchmarkSuite *models,
        #              std::vector<EstimatedCost> *costBreakdown)



        print(">>> Done.")

    refresh()
simulate()
