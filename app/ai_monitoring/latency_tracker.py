import time



class LatencyTracker:


    def start(self):

        return time.perf_counter()



    def end(

        self,

        start_time: float,

    ) -> float:


        return round(

            time.perf_counter() - start_time,

            4,

        )