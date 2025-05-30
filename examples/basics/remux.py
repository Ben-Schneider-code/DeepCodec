import quickcodec
import quickcodec.datasets

quickcodec.logging.set_level(quickcodec.logging.VERBOSE)

input_ = quickcodec.open(quickcodec.datasets.curated("pexels/time-lapse-video-of-night-sky-857195.mp4"))
output = quickcodec.open("remuxed.mkv", "w")

# Make an output stream using the input as a template. This copies the stream
# setup from one to the other.
in_stream = input_.streams.video[0]
out_stream = output.add_stream_from_template(in_stream)

for packet in input_.demux(in_stream):
    print(packet)

    # We need to skip the "flushing" packets that `demux` generates.
    if packet.dts is None:
        continue

    # We need to assign the packet to the new stream.
    packet.stream = out_stream

    output.mux(packet)

input_.close()
output.close()
