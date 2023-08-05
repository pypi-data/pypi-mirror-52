// Copyright(c) 2015-present, Gabi Melman & spdlog contributors.
// Distributed under the MIT License (http://opensource.org/licenses/MIT)

#pragma once

#ifndef SPDLOG_HEADER_ONLY
#include "spdlog/details/thread_pool.h"
#endif

#include "spdlog/common.h"

namespace spdlog {
namespace details {
SPDLOG_INLINE thread_pool::thread_pool(size_t q_max_items, size_t threads_n)
    : q_(q_max_items)
{
    if (threads_n == 0 || threads_n > 1000)
    {
        throw spdlog_ex("spdlog::thread_pool(): invalid threads_n param (valid "
                        "range is 1-1000)");
    }
    for (size_t i = 0; i < threads_n; i++)
    {
        threads_.emplace_back(&thread_pool::worker_loop_, this);
    }
}

// message all threads to terminate gracefully join them
SPDLOG_INLINE thread_pool::~thread_pool()
{
    try
    {
        for (size_t i = 0; i < threads_.size(); i++)
        {
            post_async_msg_(async_msg(async_msg_type::terminate), async_overflow_policy::block);
        }

        for (auto &t : threads_)
        {
            t.join();
        }
    }
    catch (...)
    {}
}

void SPDLOG_INLINE thread_pool::post_log(async_logger_ptr &&worker_ptr, details::log_msg &msg, async_overflow_policy overflow_policy)
{
    async_msg async_m(std::move(worker_ptr), async_msg_type::log, msg);
    post_async_msg_(std::move(async_m), overflow_policy);
}

void SPDLOG_INLINE thread_pool::post_flush(async_logger_ptr &&worker_ptr, async_overflow_policy overflow_policy)
{
    post_async_msg_(async_msg(std::move(worker_ptr), async_msg_type::flush), overflow_policy);
}

size_t SPDLOG_INLINE thread_pool::overrun_counter()
{
    return q_.overrun_counter();
}

void SPDLOG_INLINE thread_pool::post_async_msg_(async_msg &&new_msg, async_overflow_policy overflow_policy)
{
    if (overflow_policy == async_overflow_policy::block)
    {
        q_.enqueue(std::move(new_msg));
    }
    else
    {
        q_.enqueue_nowait(std::move(new_msg));
    }
}

void SPDLOG_INLINE thread_pool::worker_loop_()
{
    while (process_next_msg_()) {};
}

// process next message in the queue
// return true if this thread should still be active (while no terminate msg
// was received)
bool SPDLOG_INLINE thread_pool::process_next_msg_()
{
    async_msg incoming_async_msg;
    bool dequeued = q_.dequeue_for(incoming_async_msg, std::chrono::seconds(10));
    if (!dequeued)
    {
        return true;
    }

    switch (incoming_async_msg.msg_type)
    {
    case async_msg_type::log:
    {
        auto msg = incoming_async_msg.to_log_msg();
        incoming_async_msg.worker_ptr->backend_log_(msg);
        return true;
    }
    case async_msg_type::flush:
    {
        incoming_async_msg.worker_ptr->backend_flush_();
        return true;
    }

    case async_msg_type::terminate:
    {
        return false;
    }
    }
    assert(false && "Unexpected async_msg_type");
    return true;
}

} // namespace details
} // namespace spdlog
