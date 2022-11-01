class Payload:
    def __init__(self, topic, width, height, format="bgr", intrinsics=None):
        if intrinsics is None:
            # Dummy Camera model assuming no lense distortion and idealized camera intrinsics.
            # For 192x192 pixels.
            # intrinsics = [
            #     [1000, 0.0, 192 / 2.0],
            #     [0.0, 1000, 192 / 2.0],
            #     [0.0, 0.0, 1.0],
            # ]
            if topic=="world":
                # intrinsics = [
                #         [395.60662814306596, 0.0, 316.72212558212516],
                #         [0.0, 395.56975615889445, 259.206579702132],
                #         [0.0, 0.0, 1.0],
                #     ]
                intrinsics = [
                [794.3311439869655, 0.0, 633.0104437728625],
                [0.0, 793.5290139393004, 397.36927353414865],
                [0.0, 0.0, 1.0],
                        ]
            else :    
                intrinsics = [
                        [282.976877, 0.0, 96],
                        [0.0, 283.561467, 96],
                        [0.0, 0.0, 1.0],
                    ]
        if topic is None:
            raise Exception("topic has to be either: world, eye0 or eye1")

        self.payload = {}
        self.payload["format"] = format
        self.payload["projection_matrix"] = intrinsics
        self.payload["topic"] = "hmd_streaming." + topic
        self.payload["width"] = width
        self.payload["height"] = height

    def setPayloadParam(self, time, frame, index):
        self.payload["timestamp"] = time
        self.payload["__raw_data__"] = [frame]
        self.payload["index"] = index

    def get(self):
        #print(self.payload["topic"])
        return self.payload
