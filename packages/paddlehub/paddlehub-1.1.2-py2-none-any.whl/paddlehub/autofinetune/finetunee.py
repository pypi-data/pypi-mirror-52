from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import ast

import paddle.fluid as fluid
import paddlehub as hub
import os
from paddlehub.common.logger import logger

# yapf: disable
parser = argparse.ArgumentParser(__doc__)
parser.add_argument("--epochs", type=int, default=3, help="epochs.")
parser.add_argument("--batch_size", type=int, default=32, help="batch_size.")
parser.add_argument("--learning_rate", type=float, default=5e-5, help="learning_rate.")
parser.add_argument("--warmup_prop", type=float, default=0.1, help="warmup_prop.")
parser.add_argument("--weight_decay", type=float, default=0.01, help="weight_decay.")
parser.add_argument("--max_seq_len", type=int, default=128, help="Number of words of the longest seqence.")
parser.add_argument("--checkpoint_dir", type=str, default=None, help="Directory to model checkpoint")
parser.add_argument("--model_path", type=str, default="", help="load model path")
args = parser.parse_args()
# yapf: enable.


if __name__ == '__main__':
    # Load Paddlehub ERNIE pretrained model
    module = hub.Module(name="ernie")
    inputs, outputs, program = module.context(
        trainable=True, max_seq_len=args.max_seq_len)

    # Download dataset and use ClassifyReader to read dataset
    dataset = hub.dataset.ChnSentiCorp()
    metrics_choices = ["acc"]

    reader = hub.reader.ClassifyReader(
        dataset=dataset,
        vocab_path=module.get_vocab_path(),
        max_seq_len=args.max_seq_len)

    # Construct transfer learning network
    # Use "pooled_output" for classification tasks on an entire sentence.
    pooled_output = outputs["pooled_output"]

    # Setup feed list for data feeder
    # Must feed all the tensor of ERNIE's module need
    feed_list = [
        inputs["input_ids"].name,
        inputs["position_ids"].name,
        inputs["segment_ids"].name,
        inputs["input_mask"].name,
    ]

    # Select finetune strategy, setup config and finetune
    strategy = hub.AdamWeightDecayStrategy(
        warmup_proportion=args.warmup_prop,
        learning_rate=args.learning_rate,
        weight_decay=args.weight_decay,
        lr_scheduler="linear_decay")

    # Setup runing config for PaddleHub Finetune API
    config = hub.RunConfig(
        checkpoint_dir=args.checkpoint_dir,
        use_cuda=True,
        num_epoch=args.epochs,
        batch_size=args.batch_size,
        enable_memory_optim=True,
        strategy=strategy)

    # Define a classfication finetune task by PaddleHub's API
    cls_task = hub.TextClassifierTask(
        data_reader=reader,
        feature=pooled_output,
        feed_list=feed_list,
        num_classes=dataset.num_labels,
        config=config,
        metrics_choices=metrics_choices)

    # Finetune and evaluate by PaddleHub's API
    if args.model_path != "":
        with cls_task.phase_guard(phase="train"):
            cls_task.init_if_necessary()
            cls_task.load_parameters(args.model_path)
            logger.info("PaddleHub has loaded model from %s" % args.model_path)

    run_states = cls_task.finetune_and_eval()
    # train_avg_score, train_avg_loss, train_run_speed = cls_task._calculate_metrics(run_states)

    run_states = cls_task.eval()
    eval_avg_score, eval_avg_loss, eval_run_speed = cls_task._calculate_metrics(run_states)

print(eval_avg_score["acc"], end="")
