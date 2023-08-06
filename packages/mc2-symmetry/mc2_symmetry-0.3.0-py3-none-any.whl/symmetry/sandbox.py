import pymq
from pymq.provider.redis import RedisConfig

from symmetry.clusterd import DefaultBalancingPolicyService
from symmetry.clusterd.policies.balancing import RoundRobin


def main():
    cfg = RedisConfig()
    eventbus = pymq.init(cfg)

    rds = cfg.get_redis()

    service = DefaultBalancingPolicyService(bus=eventbus)

    service.set_active_policy(RoundRobin())



    pymq.shutdown()

if __name__ == '__main__':
    main()