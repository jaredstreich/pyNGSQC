# -*- coding: utf-8 *-*
# Copyright 2012 Kevin Murray
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import pyngsqc


class FastqToFasta(pyngsqc.Base):

    def __init__(
        self,
        in_file_name,
        out_file_name,
        remove_header=False,
        deduplicate_header=True,
        compression=pyngsqc.GUESS_COMPRESSION
    ):
        super(FastqToFasta, self).__init__(
            in_file_name,
            out_file_name,
            compression=compression,
            deduplicate_header=deduplicate_header
        )
        self.writer = pyngsqc.FastaWriter(
            self.out_file_name,
            compression
        )
        self.remove_header = remove_header

    def run(self):
        for read in self.reader:
            fasta_read = []
            if self.remove_header:
                header = ">%i" % self.stats["reader"]["num_reads"]
            else:
                header = ">%s" % read[0][1:]  # Keep fastq header

            fasta_read.append(header)
            fasta_read.append(read[1])  # Seq

            self.writer.write(fasta_read)
        self.stats["reader"] = self.reader.stats
        self.stats["writer"] = self.writer.stats


class ConvertQualOffset(pyngsqc.Base):

    def __init__(
        self,
        in_file_name,
        out_file_name,
        in_qual_offset=33,
        out_qual_offset=64,
        deduplicate_header=True,
        compression=pyngsqc.GUESS_COMPRESSION
    ):
        super(ConvertQualOffset, self).__init__(
            in_file_name,
            out_file_name,
            compression=compression,
            deduplicate_header=deduplicate_header
        )
        self.in_qual_offset = in_qual_offset
        self.out_qual_offset = out_qual_offset

    def run(self):
        for read in self.reader:
            in_phred_str = read[3]
            read[3] = pyngsqc.convert_phred_offset(
                in_phred_str,
                self.in_qual_offset,
                self.out_qual_offset
            )
            self.writer.write(read)

        self.stats["reader"] = self.reader.stats
        self.stats["writer"] = self.writer.stats
