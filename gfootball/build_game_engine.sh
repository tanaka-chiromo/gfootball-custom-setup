#!/bin/bash
# Copyright 2019 Google LLC
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

set -e

LIB_EXTENSION="so"

if [[ "$OSTYPE" == "darwin"* ]] ; then
    LIB_EXTENSION="dylib"
fi

# Use the pip/venv interpreter when provided (setup.py sets PYTHON).
PYTHON="${PYTHON:-python3}"

# Take into account # of cores and available RAM for deciding on compilation parallelism.
PARALLELISM=$($PYTHON -c '
try:
    import multiprocessing as mp
    try:
        import psutil
        print(int(max(1, min((psutil.virtual_memory().available / 1e9 - 1) / 0.5, mp.cpu_count()))))
    except Exception:
        print(max(1, mp.cpu_count() // 2 or 1))
except Exception:
    print(1)
')

# Delete pre-existing version of CMakeCache.txt to make 'python3 -m pip install' work.
rm -f third_party/gfootball_engine/CMakeCache.txt
# CMakeLists.txt declares `cmake_minimum_required(VERSION 3.4)`. CMake >=4.0
# refuses to configure at all against a <3.5 floor unless told what policy
# set to fall back to -- harmless to pass on older CMake too (just an unused
# cache entry there), so we always set it rather than relying on installers
# to know to export CMAKE_POLICY_VERSION_MINIMUM themselves.
pushd third_party/gfootball_engine && cmake -DCMAKE_POLICY_VERSION_MINIMUM=3.5 . && make -j $PARALLELISM && popd
pushd third_party/gfootball_engine && ln -sf libgame.$LIB_EXTENSION _gameplayfootball.so && popd
