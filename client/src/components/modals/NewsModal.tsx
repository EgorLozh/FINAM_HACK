"use client";
import React from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { NewsItem } from "@/types";
import { Calendar, Clock, ExternalLink, FileText, Flame, Users } from "lucide-react";
import { getHotnessColor } from "@/utils/getHotnessColor";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";

interface NewsModalProps {
  newsItem: NewsItem | null;
  isOpen: boolean;
  onClose: () => void;
}

const NewsModal = ({ newsItem, isOpen, onClose }: NewsModalProps) => {
  if (!newsItem) return null;

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="max-w-4xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle className="text-xl font-bold text-foreground">
            Детали новости
          </DialogTitle>
        </DialogHeader>
        
        <Card className="overflow-hidden border-l-4 border-l-lava/50">
          <CardHeader className="pb-6 border-b-2 border-lava">
            <div className="flex items-start justify-between gap-4">
              <CardTitle className="text-lg font-semibold text-foreground leading-tight">
                {newsItem.headline}
              </CardTitle>
              <Badge
                className={`${getHotnessColor(
                  newsItem.hotness
                )} font-medium`}
              >
                <Flame className="w-3 h-3 mr-1" />
                {newsItem.hotness}
              </Badge>
            </div>
          </CardHeader>

          <CardContent className="space-y-4 pt-3">
            {/* Почему важно сейчас */}
            <div className="space-y-2">
              <div className="flex items-center gap-2 text-sm font-medium text-muted-foreground">
                <Clock className="w-4 h-4" />
                Почему важно сейчас
              </div>
              <p className="text-sm text-foreground leading-relaxed pl-6">
                {newsItem.why_now}
              </p>
            </div>

            {/* Затронутые сущности */}
            <div className="space-y-2">
              <div className="flex items-center gap-2 text-sm font-medium text-muted-foreground">
                <Users className="w-4 h-4" />
                Затронутые сущности
              </div>
              <div className="flex flex-wrap gap-2 pl-6">
                {newsItem.entities.split(",").map((entity, idx) => (
                  <Badge key={idx} variant="secondary" className="text-xs">
                    {entity.trim()}
                  </Badge>
                ))}
              </div>
            </div>

            {/* Временные метки */}
            <div className="space-y-2">
              <div className="flex items-center gap-2 text-sm font-medium text-muted-foreground">
                <Calendar className="w-4 h-4" />
                Ключевые временные метки
              </div>
              <p className="text-sm text-foreground leading-relaxed pl-6">
                {newsItem.timeline}
              </p>
            </div>

            {/* Источники */}
            <div className="space-y-2">
              <div className="flex items-center gap-2 text-sm font-medium text-muted-foreground">
                <ExternalLink className="w-4 h-4" />
                Источники
              </div>
              <p className="text-sm text-foreground leading-relaxed pl-6">
                {newsItem.sources}
              </p>
            </div>

            {/* Черновик */}
            <div className="space-y-2">
              <div className="flex items-center gap-2 text-sm font-medium text-muted-foreground">
                <FileText className="w-4 h-4" />
                Черновик
              </div>
              <div className="bg-muted/50 rounded-lg p-4 pl-6">
                <p className="text-sm text-foreground leading-relaxed">
                  {newsItem.draft}
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      </DialogContent>
    </Dialog>
  );
};

export default NewsModal;
