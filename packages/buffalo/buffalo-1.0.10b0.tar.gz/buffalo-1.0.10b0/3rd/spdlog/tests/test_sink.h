//
// Copyright(c) 2018 Gabi Melman.
// Distributed under the MIT License (http://opensource.org/licenses/MIT)
//

#pragma once

#include "spdlog/details/null_mutex.h"
#include "spdlog/sinks/base_sink.h"

#include <chrono>
#include <mutex>
#include <thread>

namespace spdlog {
namespace sinks {

template<class Mutex>
class test_sink : public base_sink<Mutex>
{
public:
    size_t msg_counter()
    {
        std::lock_guard<Mutex> lock(base_sink<Mutex>::mutex_);
        return msg_counter_;
    }

    size_t flush_counter()
    {
        std::lock_guard<Mutex> lock(base_sink<Mutex>::mutex_);
        return flush_counter_;
    }

    void set_delay(std::chrono::milliseconds delay)
    {
        delay_ = delay;
    }

protected:
    void sink_it_(const details::log_msg &) override
    {
        msg_counter_++;
        std::this_thread::sleep_for(delay_);
    }

    void flush_() override
    {
        flush_counter_++;
    }
    size_t msg_counter_{0};
    size_t flush_counter_{0};
    std::chrono::milliseconds delay_{std::chrono::milliseconds::zero()};
};

using test_sink_mt = test_sink<std::mutex>;
using test_sink_st = test_sink<details::null_mutex>;

} // namespace sinks
} // namespace spdlog
